import torchvision
from torch import nn
import torch.optim
from torch.nn import Conv2d,MaxPool2d,Flatten,Linear
from torch.utils.data import DataLoader
train_data = torchvision.datasets.CIFAR10(root='data',train=True,transform=torchvision.transforms.ToTensor(),download=True)
test_data = torchvision.datasets.CIFAR10(root='data',train=False,transform=torchvision.transforms.ToTensor(),download=True)

train_loader = DataLoader(dataset=train_data,batch_size=64,shuffle=True,)
test_loader = DataLoader(dataset=test_data,batch_size=64)

print(type(train_data))

class Tudui(nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.model = nn.Sequential(
            Conv2d(3, 32, 5, padding=2),
            MaxPool2d(2),
            Conv2d(32, 32, 5, padding=2),
            MaxPool2d(2),
            Conv2d(32, 64, 5, padding=2),
            MaxPool2d(2),
            Flatten(),
            Linear(1024, 64),
            Linear(64, 10)
        )
    def forward(self,x):
        output = self.model(x)
        return output
tudui = Tudui()
cross = nn.CrossEntropyLoss()
optim = torch.optim.SGD(params=tudui.parameters(),lr=1e-2)
total_loss = 0
for epoch in range(20):
    for data in train_loader:
        img,label = data
        output = tudui(img)
        loss_fn = cross(output,label)

        optim.zero_grad()#优化器清零
        loss_fn.backward()#损失函数清零
        optim.step()#参数更新
def test(loader,model):
    correct = 0
    num = 0
    for data in loader:
        img,label = data
        output = tudui(img)
        correct += (output.argmax(1)==label).sum()
        num += output.size()
    return correct/num
accuracy = test(test_loader,tudui)
print('准确率是',accuracy)