## Sample

### C++ Code

```c++
int main() {
  int n = 1000;
  int sum = 0;
  int i;
  int j;
  for (i = 1; i <= n; ++i) {
    for (j = 1; j <= n; ++j)
      sum = sum ^ i;
    sum = sum & 1;
  }
  return sum;
}
```

### Optimization process

#### No Opt
<img src="no_opt.png" width = "600px"/>

#### Peephole

<img src="peephole.png" width = "600px"/>

#### Mem2Reg

<img src="mem2reg.png" width = "600px"/>