#!/usr/bin/python3
import os
from os.path import join as osjoin

import unittest

from enum import Enum

# Use these to distinguish node types, note that you might want to further
# distinguish between the addition and multiplication operators
NodeType = Enum('BinOpNodeType', ['number', 'operator'])


class TestBench(unittest.TestCase):
    testDir = [osjoin('testbench','arith_id'), osjoin('testbench','mult_id'), 
            osjoin('testbench','mult_by_zero'),osjoin('testbench','combined')]
    def test(self):
        for testType in self.testDir:
            inputDir = osjoin(testType, 'inputs')
            outputDir = osjoin(testType, 'outputs')
            for file in os.listdir(outputDir):
                ins = osjoin(inputDir, file)
                outs = osjoin(outputDir, file)        #Mirrored input output filename

                with open(ins) as r:
                    inputValue = r.read().split()
                with open(outs) as r:
                    outputValue = r.read()
                with self.subTest(msg = "Test " + str(file), inputValue = inputValue, outputValue = outputValue):
                    current = BinOpAst(inputValue)
                    current.simplify_binops()
                    ans = current.prefix_str()
                    self.assertEqual(ans, outputValue) #Tests two values are equal    

        



class BinOpAst():
    """
    A somewhat quick and dirty structure to represent a binary operator AST.

    Reads input as a list of tokens in prefix notation, converts into internal representation,
    then can convert to prefix, postfix, or infix string output.
    """
    def __init__(self, prefix_list):
        """
        Initialize a binary operator AST from a given list in prefix notation.
        Destroys the list that is passed in.
        """
        self.val = prefix_list.pop(0)
        if self.val.isnumeric():
            self.type = NodeType.number
            self.left = False
            self.right = False
        else:
            self.type = NodeType.operator
            self.left = BinOpAst(prefix_list)
            self.right = BinOpAst(prefix_list)

    def __str__(self, indent=0):
        """
        Convert the binary tree printable string where indentation level indicates
        parent/child relationships
        """
        ilvl = '  '*indent
        left = '\n  ' + ilvl + self.left.__str__(indent+1) if self.left else ''
        right = '\n  ' + ilvl + self.right.__str__(indent+1) if self.right else ''
        return f"{ilvl}{self.val}{left}{right}"

    def __repr__(self):
        """Generate the repr from the string"""
        return str(self)

    def prefix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        # if self == False:
        match self.type:
            case NodeType.number:
                return str(self.val)
            case NodeType.operator:
                if self.right == False or self.left == False:
                    return str(self.val)
                else:
                    return str(self.val) + ' ' + self.left.prefix_str() + ' ' + self.right.prefix_str()
            

    def infix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return '(' + self.left.infix_str() + ' ' + self.val + ' ' + self.right.infix_str() + ')'
    def postfix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return str(self.val)
            case NodeType.operator:
                return self.left.postfix_str() + ' ' + self.right.postfix_str() + ' ' + self.val

    def additive_identity(self):
        """
        Reduce additive identities
        x + 0 = x
        """
        # In prefix: + x 0 simplify to x
        if self.right == False:                 #Base case once last number reached
            return
        if self.type == NodeType.operator:      #Instead change to node type is operator 
            self.right.additive_identity()      #Will reach from the bottom
        if self.val == '+':
            if self.right.val == '0':
                self.val = self.left.val
                self.right = False
                self.left = False
            elif self.left.val == '0':
                self.val = self.right.val            
                self.right = False
                self.left = False    
        # IMPLEMENT ME!
        pass
                        
    def multiplicative_identity(self):
        """
        Reduce multiplicative identities
        x * 1 = x
        """
        if self.right == False:
            return
        if self.type == NodeType.operator:      
            self.right.multiplicative_identity()  
        if self.val == '*':
            if self.right.val == '1':
                self.val = self.left.val
                self.right = False
                self.left = False
            elif self.left.val == '1':
                self.val = self.right.val            
                self.right = False
                self.left = False    
        # IMPLEMENT ME!
        pass
    
    
    def mult_by_zero(self):
        """
        Reduce multiplication by zero
        x * 0 = 0
        """
        if self.right == False: 
            return
        if self.type == NodeType.operator:     
            self.right.mult_by_zero()  
        if self.val == '*':
            if self.right.val == '0' or self.left.val == '0':
                self.val = '0'
                self.right = False
                self.left = False 
        # Optionally, IMPLEMENT ME! (I'm pretty easy)
        pass
    
    def constant_fold(self):
        """
        Fold constants,
        e.g. 1 + 2 = 3
        e.g. x + 2 = x + 2
        """
        # Optionally, IMPLEMENT ME! This is a bit more challenging. 
        # You also likely want to add an additional node type to your AST
        # to represent identifiers.
        pass            

    def simplify_binops(self):
        """
        Simplify binary trees with the following:
        1) Additive identity, e.g. x + 0 = x
        2) Multiplicative identity, e.g. x * 1 = x
        3) Extra #1: Multiplication by 0, e.g. x * 0 = 0
        4) Extra #2: Constant folding, e.g. statically we can reduce 1 + 1 to 2, but not x + 1 to anything
        """
        self.mult_by_zero()
        self.additive_identity()
        self.multiplicative_identity()
        self.constant_fold()

        # Run through identites again to further simplify

        self.mult_by_zero()
        self.additive_identity()
        self.multiplicative_identity()
        self.constant_fold()


# test = BinOpAst(['+','5', '0'])
# print(test)
# test.simplify_binops()
# stre = test.prefix_str()
# print(str)

if __name__ == "__main__":
    unittest.main()
