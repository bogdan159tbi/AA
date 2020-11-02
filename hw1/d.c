#include<stdio.h>
#include<stdlib.h>
#include<string.h>
int main(void){
	FILE *f = fopen("output","rw");
	char c[200];
	FILE *o = fopen("out","rw");
	if(!o)
	{
	fprintf(stderr,"nu s a deschis\n");
	return -1;
	}

	while(fgets(c,20,f)){
	c[strlen(c)-1] = '\0';
	printf("%s ",c);
	}
	return 0;
}
