#include<stdio.h>
#include<stdlib.h>
#include<string.h>

#pragma pack(8)
struct MPK_Head {
    char sign[4];
    unsigned int a;
    unsigned int number;
    char unknow[0x34];
} mpk_head;
struct MPK_Index {//0xa0
    unsigned int count;
    unsigned long long index;
    unsigned long long length;
    unsigned long long length_1;
    char name[0xe0];
} *mpk_index;
#pragma pack()


int main(int argc,char* argv[])
{
    if (argc!=2)
        return 0;
    FILE* input=fopen(argv[1],"rb");
    char name[0xa0];
    fread(&mpk_head,sizeof(struct MPK_Head),1,input);
    if (strcmp(mpk_head.sign,"MPK")){
        printf("unknow file type!");
        return 0;
    }
    strcpy(name,argv[1]);
    int len=strlen(argv[1])-3;
    name[len]='\0';
    name[len-1]='\0';
    char command[0xa0];
    sprintf(command,"mkdir %s",name);
    system(command);
    name[len-1]='/';
    mpk_index=malloc((size_t)(sizeof(struct MPK_Index)*mpk_head.number));
    fread(mpk_index,sizeof(struct MPK_Index),mpk_head.number,input);
    for (int i=0;i<mpk_head.number;i++){
        fseek(input,mpk_index[i].index,SEEK_SET);
        //printf("%llx%llx",mpk_index[i].index,mpk_index[i].length);
        strcpy(name+len,mpk_index[i].name);
        name[len+strlen(mpk_index[i].name)]='\0';
        FILE* out=fopen(name,"wb");
        puts(name);
        char *tmp=malloc(sizeof(char)*mpk_index[i].length);
        fread(tmp,1,mpk_index[i].length,input);
        fwrite(tmp,1,mpk_index[i].length,out);
        fclose(out);
        free(tmp);
    }
    free(mpk_index);
    return 0;
}

