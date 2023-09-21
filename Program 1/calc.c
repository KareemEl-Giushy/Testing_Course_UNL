#include<stdio.h>

typedef struct {
    char op;
    float n1;
    float n2;
} expr;

float calc(expr a) {
    switch (a.op) {
    case '+':
        return a.n1 + a.n2;
    case '-':
        return a.n1 - a.n2;
    case '*':
        return a.n1 * a.n2;
    case '/':
        return a.n1 / a.n2;
    default:
        printf("invalid operator. calc only supports: + - * /\n");
        return 0;
    }
}

int main(int argc, char **argv) {
    if (argc == 1) {
        printf("use: ./calc <expr>\n");
        return 0;
    }

    for (int i = 1; i < argc; i++) {
        expr str1;
        int err = sscanf(argv[i], "%f %c %f", &str1.n1, &str1.op, &str1.n2);

        if (err != 3) {
            printf("wrong format!\n");
        } else {
            printf("%s = %f\n", argv[i], calc(str1));
        }
    }

    return 0;
}
