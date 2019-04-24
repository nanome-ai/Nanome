from . import Vector3

import random
import operator
import sys
import unittest

class MatrixException(Exception):
    pass

class Matrix(object):
    def __init__(self, m, n):
        self.__rows = [[0] * n for i in range(m)]
        self.__m = m
        self.__n = n
        
    def __getitem__(self, m):
        return self.__rows[m]

    def __setitem__(self, m, row):
        self.__rows[m] = row
        
    def __str__(self):
        s = '\n'.join([' '.join([str(item) for item in row]) for row in self.__rows])
        return s + '\n'

    def __eq__(self, matrix):
        return matrix.__rows == self.__rows
        
    def __add__(self, matrix):
        if self.get_rank() != matrix.get_rank():
            raise MatrixException("Only matrices of same rank can be added")

        result = Matrix(self.__m, self.__n)
        
        for i in range(self.__m):
            result[i] = [cur[0] + cur[1] for cur in zip(self.__rows[i], matrix[i])]

        return result

    def __sub__(self, matrix):
        if self.get_rank() != matrix.get_rank():
            raise MatrixException("Only matrices of same rank can be subtracted")

        result = Matrix(self.__m, self.__n)
        
        for i in range(self.__m):
            result[i] = [cur[0] - cur[1] for cur in zip(self.__rows[i], matrix[i])]

        return result

    def __mul__(self, matrix):
        if isinstance(matrix, Vector3):
            matrix = Matrix.from_vector3(matrix)

        rank_m, rank_n = matrix.get_rank()
        if self.__n != rank_m:
            raise MatrixException("Trying to multiply a matrix with n=" + str(self.__n) + " by a matrix with m=" + str(rank_m))
        
        transpose = matrix.get_transpose()
        result = Matrix(self.__m, rank_n)
        
        for i in range(self.__m):
            for j in range(transpose.__m):
                result[i][j] = sum([cur[0] * cur[1] for cur in zip(self.__rows[i], transpose[j])])

        return result

    def __iadd__(self, matrix):
        if self.get_rank() != matrix.get_rank():
            raise MatrixException("Only matrices of same rank can be added")

        for i in range(self.__m):
            for j in range(self.__n):
                self.__rows[i][j] += matrix.__rows[i][j]
        return self

    def __isub__(self, matrix):
        if self.get_rank() != matrix.get_rank():
            raise MatrixException("Only matrices of same rank can be subtracted")

        for i in range(self.__m):
            for j in range(self.__n):
                self.__rows[i][j] -= matrix.__rows[i][j]
        return self

    def transpose(self):
        self.__m, self.__n = self.__n, self.__m
        self.__rows = Matrix.__transpose_rows(self.__rows, self.__m, self.__n)
        return self

    def get_transpose(self):
        result = Matrix(self.__m, self.__n)
        result.__rows = Matrix.__transpose_rows(self.__rows, self.__m, self.__n)
        return result

    @staticmethod
    def __transpose_rows(rows, m, n):
        return [[rows[j][i] for j in range(m)] for i in range(n)]

    def get_minor(self, i, j):
        result = Matrix(i, j)
        result.__rows = [row[:j] + row[j+1:] for row in (self.__rows[:i] + self.__rows[i+1:])]
        return result

    def get_determinant(self):
        rows = self.__rows
        if self.__m == 2 and self.__n == 2:
            return rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]

        result = 0
        for j in range(self.__n):
            result += ((-1) ** j) * rows[0][j] * self.get_minor(0, j).get_determinant()
        return result

    def get_inverse(self):
        determinant = self.get_determinant()
        rows = self.__rows
        if self.__m == 2 and self.__n == 2:
            return [[rows[1][1] / determinant, -rows[0][1] / determinant], [-rows[1][0] / determinant, rows[0][0] / determinant]]

        result = Matrix(self.__m, self.__n)
        for i in range(self.__m):
            for j in range(self.__n):
                minor = self.get_minor(i, j)
                result[i][j] = (((-1) ** (i + j)) * minor.get_determinant()) / determinant
        result.transpose()
        return result

    def get_rank(self):
        return (self.__m, self.__n)

    @classmethod
    def identity(cls, size):
        result = cls(size, size)
        for i in range(size):
            result.__rows[i][i] = 1
        return result

    @classmethod
    def from_vector3(cls, vector):
        result = cls(4, 1)
        result[0][0] = vector.x
        result[1][0] = vector.y
        result[2][0] = vector.z
        result[3][0] = 1
        return result