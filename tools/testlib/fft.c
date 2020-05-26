#include <stdio.h>
#include <stdlib.h>

int P = 998244353;
int G = 3;

int maxN = 262145;
int n;
int m;
int S;
int L;
int invN;

int i, j, k;
int *a;
int *b;
int *c;
int *wn;
int *rev;


int fast_mul(int x, int d) {
  int ret = 0;
  while (d > 0) {
    if ((d & 1) == 1)
      ret = (ret + x) % P;
    d = d >> 1;
    x = (x + x) % P;
  }
  return ret;
}

int fast_pow(int x, int d) {
  int ret = 1;
  while (d > 0) {
    if ((d & 1) == 1)
      ret = fast_mul(ret, x);
    d = d >> 1;
    x = fast_mul(x, x);
  }
  return ret;
}

int init(int n) {
  a = malloc(sizeof(int) * maxN);
  b = malloc(sizeof(int) * maxN);
  c = malloc(sizeof(int) * maxN);
  wn = malloc(sizeof(int) * maxN);
  rev = malloc(sizeof(int) * maxN);
  
  L = 1;
  S = 0;
  for (; L <= n; ) { L = L << 1; ++S; }
  
  for (i = 1; i < L; ++i)
    rev[i] = (rev[i >> 1] >> 1) | ((i & 1) << (S - 1));
  wn[0] = 1;
  wn[1] = fast_pow(G, (P - 1) / L);
  for (i = 2; i <= L; ++i)
    wn[i] = fast_mul(wn[i - 1], wn[1]);
  invN = fast_pow(L, P - 2);
}

void dft(int *a,int tp) {
  for (i = 0; i < L; ++i)
    if (i < rev[i]) {
      int tmp = a[i];
      a[i] = a[rev[i]];
      a[rev[i]] = tmp;
    }

  for (k = 1; k < L; k = k << 1) {
    int k2 = k << 1;
    for (i = 0; i < L; i = i + k2)
      for (j = 0; j < k; ++j) {
	int x = a[i + j];
	int y = a[i + j + k];
        if (tp > 0) 
          y = fast_mul(y, wn[L / k2 * j]);
        else
          y = fast_mul(y, wn[L - L / k2 * j]);
	a[i + j] = (x + y) % P;
	a[i + j + k] = (x - y + P) % P;
      }
  }

  if (tp < 0)
    for (i = 0; i < L; ++i) a[i] = fast_mul(a[i], invN);
}

int getInt() {
  int x;
  scanf("%d\n", &x);
  return x;
}
 
int main() {
  n = getInt();
  m = getInt();

  init(n + m);
  for (i = 0; i <= n; ++i)
    a[i] = getInt();
  for (i = 0; i <= m; ++i)
    b[i] = getInt();

  dft(a, 1);
  dft(b, 1);

  for (i = 0; i < L; ++i)
    c[i] = fast_mul(a[i], b[i]);

  dft(c, -1);

  int res = 0;
  for (i = 0; i <= n + m; ++i)
    res = res ^ c[i];
  printf("%d", res);

  return 0;
}
 
