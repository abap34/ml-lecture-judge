# Solution
import numpy as np


class Variable:
    def __init__(self, data, name=''):
        self.data = data
        self.grad = None
        self.creator = None
        self.name = name

    def backward(self):
        if self.grad is None:
            self.grad = np.ones_like(self.data)
        funcs = [self.creator]
        while funcs:
            f = funcs.pop()
            y = f.output
            inputs = f.inputs
            grads = f.backward(y.grad)

            # 各入力に勾配を詰めていく
            if not isinstance(grads, tuple):
                grads = (grads, )

            for input, grad in zip(inputs, grads):
                input.grad = grad
                if input.creator is not None:
                    funcs.append(input.creator)


    def __mul__(self, other):
        return mul(self, other)

    def __rmul__(self, other):
        return mul(other, self)

    def __repr__(self):
        return 'Variable(' + str(self.data).replace('array', '') + ')'



class Function:
    def __call__(self, *inputs):
        self.inputs = inputs
        xs = [input.data for input in inputs]
        y = self.forward(*xs)
        output = Variable(y)
        output.creator = self
        self.output = output
        return output

    def forward(self, *inputs):
        raise NotImplementedError()

    def backward(self, gy):
        raise NotImplementedError()


class Exp(Function):
    def forward(self, x):
        return np.exp(x)

    def backward(self, gy):
        return gy * np.exp(gy)


def exp(x):
    f = Exp()
    return f(x)


class Mul(Function):
    def forward(self, x, y):
        return x * y

    def backward(self, gy):
        x = self.inputs[0].data
        y = self.inputs[1].data
        return gy * y, gy * x


def mul(x, y):
    f = Mul()
    return f(x, y)


class Sigmoid(Function):
    def __init__(self):
        self.y = None

    def forward(self, x):
        y = 1 / (1 + np.exp(-x))
        self.y = y
        return y

    def backward(self, gy):
        y = self.y
        return gy * y * (y - 1)


def sigmoid(x):
    f = Sigmoid()
    return f(x)



x = list(map(float, input().split()))
w1 = list(map(float, input().split()))
w2 = list(map(float, input().split()))


# ①定義
x = Variable(np.array(x))
w1 = Variable(np.array(w1))
w2 = Variable(np.array(w2))


# ②計算
# 一層目
h1 = x * w1
a1 = sigmoid(h1)
# 二層目
h2 = a1 * w2
y = sigmoid(h2)


# ③ backward
y.backward()

print(w1.grad, w2.grad)



# グラフ描画用の関数たち 問題とは関係ない
def _dot_var(v):
    name = v.name if v.name is not None else ''
    dot_var = f'{id(v)} [label="{name}", color=lightblue, style=filled]\n'
    return dot_var

def _dot_func(f):
    name = f.__class__.__name__
    dot_func = f'{id(f)} [label="{name}", color=gray, style=filled, shape=box]\n'
    dot_edge = '{} -> {}\n'
    for input in f.inputs:
        dot_func += dot_edge.format(id(input), id(f))
    dot_func += dot_edge.format(id(f), id(f.output))
    return dot_func

def make_graphviz_script(y):
    dot_script = _dot_var(y)
    funcs = [y.creator]
    while funcs:
        f = funcs.pop()
        dot_script += _dot_func(f)
        for input in f.inputs:
            dot_script += _dot_var(input)
            if input.creator is not None:
                funcs.append(input.creator)
    return 'digraph g {\n graph [rankdir = LR];\n' + dot_script + '}'

# 以下をコメントアウトしてターミナルで次のコマンドを実行するとグラフを作成できる
# dot graph_example.dot  -T png -o example.png -Gdpi=600
#
# x.name = 'x'
# w1.name = 'w1'
# w2.name = 'w2'
# h1.name = 'h1'
# h2.name = 'h2'
# a1.name = 'a1'
# y.name = 'y'
#
# dot_script = make_graphviz_script(y)
# with open('graph_example.dot', 'w+') as f:
#     f.write(dot_script)
