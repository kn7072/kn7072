int AddIntInt(int a, int b);
int AddIntStr(int a, const char *b);
int AddStrInt(const char *a, int b);
int AddStrStr(const char *a, const char *b);

// clang-format off
#define AddStr(y)                  \
  _Generic((y), int:    AddStrInt, \
                char *: AddStrStr, \
          const char *: AddStrStr)

#define AddInt(y)                  \
  _Generic((y), int:    AddIntInt, \
                char *: AddIntStr, \
          const char *: AddIntStr)

#define Add(x, y)                  \
  _Generic((x), int:    AddInt(y), \
                char *: AddStr(y), \
          const char *: AddStr(y))((x), (y))

// clang-format on
