#pragma once
#include <vector>

extern "C" double scalar_product(double *a, double *b, int now_row, int columns);
    /**
        求两个向量的内积
        @param a 第一个向量
        @param b 第二个向量
        @return 两个向量的内积
    */

extern "C" int search(double *query_matrix, double *query_text, int rows, int columns);
    /**
        根据查询矩阵查找最相似的文本嵌入。
        @param query_matrix 第一个向量
        @param query_text 第二个向量
        @return 两个向量的内积
    */