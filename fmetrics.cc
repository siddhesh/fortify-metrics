// SPDX-License-Identifier: MIT

#include <gcc-plugin.h>
#include <plugin-version.h>

#include <builtins.h>
#include <context.h>
#include <tree.h>
#include <tree-cfgcleanup.h>
#include <tree-object-size.h>
#include <tree-pass.h>
#include <tree-pretty-print.h>
#include <gimple.h>
#include <gimple-iterator.h>
#include <gimple-fold.h>

int plugin_is_GPL_compatible;

static size_t total;
static size_t bos;
static size_t bdos;
char *project;

static struct plugin_info fmetrics_info = {
  .version = "1",
  .help = "Get __builtin_object_size success metrics",
};

const pass_data pass_data_fmetrics =
{
  GIMPLE_PASS, /* type */
  "fmetrics", /* name */
  OPTGROUP_NONE, /* optinfo_flags */
  TV_NONE, /* tv_id */
  ( PROP_cfg | PROP_ssa ), /* properties_required */
  0, /* properties_provided */
  0, /* properties_destroyed */
  0, /* todo_flags_start */
  0, /* todo_flags_finish */
};

class pass_fmetrics : public gimple_opt_pass
{
public:
  pass_fmetrics (gcc::context *ctx) : gimple_opt_pass (pass_data_fmetrics, ctx)
  {
  }

  opt_pass *clone () final override
  {
    return new pass_fmetrics (m_ctxt);
  }

  unsigned int execute (function *fun) final override;
};

gimple_opt_pass *
make_pass_fmetrics (gcc::context *ctx)
{
  return new pass_fmetrics (ctx);
}

void
compile_done (void *d1, void *d2)
{
  fprintf (stderr, "%s:: %zu:%zu:%zu\n", project, total, bos, bdos);
  free (project);
}

int
plugin_init (struct plugin_name_args *info, struct plugin_gcc_version *ver)
{
  if (!plugin_default_version_check (ver, &gcc_version))
    return -1;

  /* We take only one argument.  */
  if (info->argc == 1 && !strcmp (info->argv[0].key, "project"))
    project = __builtin_strdup (info->argv[0].value);
  else
    project = __builtin_strdup ("UNKNOWN");

  gimple_opt_pass *pass_fmetrics = make_pass_fmetrics (g);
  register_pass (pass_fmetrics, PASS_POS_INSERT_BEFORE, "objsz", 1);
  register_callback ("fmetrics", PLUGIN_INFO, NULL, &fmetrics_info);
  register_callback ("fmetrics", PLUGIN_FINISH, compile_done, NULL);
  return 0;
}

/* Right before objsz2, walk through and look for __builtin_object_size.
   Compute dynamic object size for that and also the static object size to mark
   coverage.  This misses ADDR_EXPRs that get computed and replaced before
   objsz2 is reached, but those are trivial transformations anyway and will
   affect both __builtin_object_size and __builtin_dynamic_object_size
   equally.  */

static size_t
get_object_size (tree ptr, int object_size_type)
{
  tree res = NULL_TREE;

  if (compute_builtin_object_size (ptr, object_size_type, &res))
    return 1;

  return 0;
}

unsigned int
pass_fmetrics :: execute (function *fun)
{
  basic_block bb;
  unsigned int todo = 0;

  FOR_EACH_BB_FN (bb, fun)
    {
      gimple_stmt_iterator i;
      for (i = gsi_start_bb (bb); !gsi_end_p (i); gsi_next (&i))
	{
	  gimple *call = gsi_stmt (i);
	  if (!gimple_call_builtin_p (call, BUILT_IN_OBJECT_SIZE)
	      && !gimple_call_builtin_p (call, BUILT_IN_DYNAMIC_OBJECT_SIZE))
	    continue;

	  tree lhs = gimple_call_lhs (call);
	  if (!lhs)
	    continue;

	  init_object_sizes ();

	  /* The result if it were a __bdos.  Build a call expression and pass
	     it.  This will generate some cruft for the compiler to clean up
	     but it's all for a good cause.  */
	  tree ptr = gimple_call_arg (call, 0);
	  tree ost = gimple_call_arg (call, 1);

	  /* Bail out on anything that is not a valid maximum object size
	     type.  */
	  if (TREE_CODE (ost) != INTEGER_CST
	      || tree_int_cst_sgn (ost) < 0
	      || compare_tree_int (ost, 1) > 0)
	    continue;

	  int object_size_type = tree_to_shwi (ost);

	  total++;
	  bos += get_object_size (ptr, object_size_type);
	  bdos += get_object_size (ptr, object_size_type | OST_DYNAMIC);
	}
    }

  fini_object_sizes ();

  if (cleanup_tree_cfg (TODO_update_ssa_only_virtuals))
    todo |= TODO_update_ssa_only_virtuals;

  return todo;
}
