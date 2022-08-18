typedef __SIZE_TYPE__ size_t;

size_t
__attribute__ ((access, __read_write__, 1, 2))
f1 (const char *c, size_t s)
{
  return __builtin_object_size (c, 0);
}

size_t
f2 (size_t s)
{
  char *obj = __builtin_malloc (s);

  return __builtin_object_size (s, 0);
}

size_t
f3 (int cond)
{
  char buf[24];
  char *obj = buf;

  if (cond)
    obj = malloc (48);;

  return __builtin_object_size (s, 0);
}
