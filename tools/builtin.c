#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void print(char*);
void println(char*);
void printInt(int);
void printlnInt(int);

int getInt();
char* getString();
char* toString(int);

char* _string_substring(char*, int, int);
int _string_parseInt(char*);
int _string_ord(char*, int);
char* _string_add(char*, char*);

void print(char* str) {
  int len = *(int*)(str-4);
  for (int i = 0; i < len; ++i)
    putchar(str[i]);
}

void println(char* str) {
  print(str);
  putchar('\n');
}

void printInt(int x) {
  char buf[64], *top = buf;
  if (x < 0) {
    putchar('-');
    x = -x;
  }
  do {
    *top++ = x % 10;
    x /= 10;
  } while(x);

  while (top != buf) 
    putchar(*--top + '0');
}

void printlnInt(int x) {
  printInt(x);
  putchar('\n');
}

int getInt() {
  int x = 0;
  scanf("%d", &x);
  return x;
}

char* getString() {
  char buf[128];
  scanf("%s", buf);

  int len = strlen(buf);

  char* s = (char*) malloc(len + 4);
  *(int*)s = len;
  strcpy(s + 4, buf);
  return s + 4;
}

char* toString(int x) {
  char buf[64], *top = buf;
  int flag = 0;
  if (x < 0) {
    flag = 1;
    x = -x;
  }
  do {
    *top++ = x % 10;
    x /= 10;
  } while (x);
  
  char*s = (char*) malloc(64);
  *(int*)s = top - buf + flag;

  s += 4;
  if (flag) *s = '-';
  for (int i = 0; top != buf; i++)
    s[i+flag] = *--top + '0';
  return s;
}

char* _string_substring(char* s, int l, int r) {
  char* a = (char*) malloc(r - l + 4);
  *(int*) a = r - l;

  a += 4;
  for (int i = l; i < r; ++i)
    a[i - l] = s[i];
  return a;
}

int _string_parseInt(char* s) {
  int x = 0;
  while (*s >= '0' && *s <= '9') 
    x = x * 10 + *s++ - '0';
  return x;
}

int _string_ord(char* s, int x) {
  return *(s + x);
}

char* _string_add(char *a, char* b) {
  int len_a = *(int *)(a - 4);
  int len_b = *(int *)(b - 4);
  char *c = (char*) malloc(len_a + len_b + 4);
  *(int *) c = len_a + len_b;
  strcpy(c + 4, a);
  strcpy(c + 4 + len_a, b);
  return c + 4;
}
