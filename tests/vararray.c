typedef __SIZE_TYPE__ size_t;

size_t
foo (size_t sz)
{
  int *buf[sz];
  return __builtin_object_size (buf, 0);
}
