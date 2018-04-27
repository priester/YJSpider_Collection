from keras.datasets import mnist
import numpy as np
from keras.models import  Sequential
from keras.layers import Dense,Dropout,Activation,Reshape,Embedding,LSTM,RNN
from keras.optimizers import SGD,Adam
from keras.utils import np_utils
(X_train, Y_train),(X_test, Y_test) = mnist.load_data()

print('原数据结构：')
print(X_train.shape, Y_train.shape)
print(X_test.shape, Y_test.shape)

#分为10个类别
nb_classes= 10
x_train_1 = X_train.reshape(60000,784)
y_train_1 = np_utils.to_categorical(Y_train,nb_classes)
print('变换后的数据结构：')
print(x_train_1.shape, y_train_1.shape)

x_test_1 = X_test.reshape(10000, 784)
y_test_1 = np_utils.to_categorical(Y_test, nb_classes)
print(x_test_1.shape, y_test_1.shape)


def simple_model():
    # 构建一个深度学习的模型
    model = Sequential()
    # 输入层，特征数量为784。
    model.add(Dense(nb_classes, input_shape=(784,)))
    # 输出层
    model.add(Activation('softmax'))

    # 设置学习速率为0.005
    sgd = SGD(lr=0.005)

    # 编译,loss 为损失函数也称为误差函数
    model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])

    model.fit(x_train_1, y_train_1)

    # model.summary()

    # 评价准确率
    print(model.metrics_names)
    model.evaluate(x_test_1, y_test_1)


def five_layers_neatural_work():
    # neural network with 5 layers
    #
    # · · · · · · · · · ·       (input data, flattened pixels)       X [batch, 784]   # 784 = 28*28
    # \x/x\x/x\x/x\x/x\x/    -- fully connected layer (relu)         W1 [784, 200]      B1[200]
    #  · · · · · · · · ·                                             Y1 [batch, 200]
    #   \x/x\x/x\x/x\x/      -- fully connected layer (relu)         W2 [200, 100]      B2[100]
    #    · · · · · · ·                                               Y2 [batch, 100]
    #    \x/x\x/x\x/         -- fully connected layer (relu)         W3 [100, 60]       B3[60]
    #     · · · · ·                                                  Y3 [batch, 60]
    #     \x/x\x/            -- fully connected layer (relu)         W4 [60, 30]        B4[30]
    #      · · ·                                                     Y4 [batch, 30]
    #      \x/               -- fully connected layer (softmax)      W5 [30, 10]        B5[10]
    #       ·                                                        Y5 [batch, 10]

    # Dropout是指对于神经网络单元按照一定的概率将其暂时从网络中丢弃, 从而解决过拟合问题。
    model = Sequential()
    model.add(Dense(200,input_shape=(784,)))
    # 使用relu激活函数
    model.add(Activation('relu'))
    model.add(Dense(100))
    model.add(Activation('relu'))
    model.add(Dropout(0.25))  # 添加一个dropout层, 随机移除25%的单元
    model.add((Dense(60)))
    model.add(Activation('relu'))
    model.add(Dropout(0.25))  # 添加一个dropout层, 随机移除25%的单元
    model.add(Dense(30))
    model.add(Activation('relu'))
    model.add(Dropout(0.25))  # 添加一个dropout层, 随机移除25%的单元
    model.add(Dense(10))
    model.add(Activation('softmax'))

    sgd = Adam(lr=0.001)
    model.compile(loss='binary_crossentropy',optimizer=sgd,metrics=['accuracy'])
    model.summary()


    # 进行训练
    model.fit(x_train_1,y_train_1,epochs=10)

    # 评价


    model.evaluate(x_test_1,y_test_1,verbose=1,batch_size=100)


five_layers_neatural_work()