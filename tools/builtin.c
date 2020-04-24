#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

void print(char*);
void println(char*);
void printInt(int);
void printlnInt(int);

int getInt();
char* getString();
char* toString(int);

struct string* _string_substring(struct string*, int, int);
int _string_parseInt(struct string*);
int _string_ord(struct string*, int);

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
  while (x) {
    *top++ = x % 10;
    x /= 10;
  }

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

  while (x) {
    *top++ = x % 10;
    x /= 10;
  }
  
  char*s = (char*) malloc(64);
  *(int*)s = top - buf;

  s += 4;
  for (int i = 0; top != buf; i++)
    s[i] = *--top;
  return s;
}

//struct string* _string_substring(
