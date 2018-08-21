#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

int angles[6];

void parser(char *line){
    // Takes in a char*, converts char* to int, comma separated
    const char *delim = ",";
    char *p = strtok(line, delim);
    int counter = 0;
    while (p != NULL){
        // convert *p to int, store into angles[counter]
        angles[counter] = atoi(p);
        // fetch next one
        p = strtok(NULL, delim);
        counter++;
    }
    assert(counter==6);
}

int main(int argc, char **argv){
    // printf("hi");
    char line[] = "1,2,3,4,5,6";
    parser(line);
    for (int i = 0; i < 6; i ++){
        printf("%d ,", angles[i]);
    }
}

