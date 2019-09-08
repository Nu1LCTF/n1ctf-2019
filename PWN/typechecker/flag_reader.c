#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define CAPTCHA_LEN 30

char captcha[100];
char userinp[100];
char* ctbl = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

int main(int argc, char* argv[], char* envp[]) {
  setbuf(stdin, NULL);
  setbuf(stdout, NULL);
  srand(time(NULL));
  memset(captcha, 0, sizeof(captcha));

  unsigned int len = strlen(ctbl);
  for(int i = 0; i < CAPTCHA_LEN; i++) {
    captcha[i] = ctbl[rand() % len];
  }

  printf("Please enter '%s': ", captcha);
  scanf("%100s", userinp);

  if(strcmp(captcha, userinp)) {
    printf("Wrong captcha!\n");
    return 1;
  }

  FILE* fp = fopen("/flag", "rb");
  if(!fp) {
    printf("Cannot open flag file, contact admin.\n");
    return 1;
  }

  char flag[100];
  memset(flag, 0, sizeof(flag));
  if(!fgets(flag, 100, fp)) {
    printf("Cannot read flag file, contact admin.\n");
    return 1;
  }

  printf("Here is your flag: %s\n", flag);
  fclose(fp);
  return 0;
}
