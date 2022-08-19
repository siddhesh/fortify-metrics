typedef __SIZE_TYPE__ size_t;

size_t
estimate (void)
{
  char *buf = __builtin_malloc (42);
  return __builtin_object_size (buf, 2);
}
