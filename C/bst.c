#include <math.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct BST BST;

struct BST {
    int key;
    BST* left;
    BST* right;
    int height;
};

BST* create(int key) {
    BST bst = {key, NULL, NULL, 1};
    return &bst;
}

void insert(BST* tree, int key) {
    if (!tree) {
        tree = create(key);
        return;
    }
    if (tree->key == key) {
        return;
    }
    if (tree->key < key) {
        insert(tree->right, key);
    } else {
        insert(tree->left, key);
    }
    tree->height = 1 + fmax(getHeight(tree->left), getHeight(tree->right));
}

/*
void insertArr(BST* tree, int* arr, int len) {
    for (int i = 0; i < len; insert(tree, arr[i++]));
} */

void delete(BST* tree, int key) {
    if (!tree) {
        return;
    }
    if (key < tree->key) {
        delete(tree->left, key);
    } else if (key > tree->key) {
        delete(tree->right, key);
    } else {
        if (!tree->left) {
            tree = tree->right;
            return;
        } else {
            tree = tree->left;
            return;
        }
        BST* tmp;
    }
}

int getHeight(BST* node) {
    if (!node) {
        return 0;
    }
    return node->height;
}

BST* minValue(BST* node) {
    BST* current = node;
}

int main(void) {
    printf("Hello world\n");
    BST root;
    root.key = 1;
}