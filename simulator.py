from abc import ABC, abstractmethod
from enum import Enum, auto
from random import random


class 行動(Enum):
    黙秘 = auto()
    自白 = auto()


class 利得:
    def __init__(self) -> None:
        pass

    def 計算(self, 囚人1の行動: 行動, 囚人2の行動: 行動):
        if 囚人1の行動 == 行動.黙秘:
            if 囚人2の行動 == 行動.黙秘:
                return (-2, -2)

            return (-10, 0)

        if 囚人2の行動 == 行動.黙秘:
            return (0, -10)

        return (-5, -5)


class 囚人(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.利得 = 0
        self.今回の行動 = None

    def 行動(self):
        self.今回の行動 = self._行動を決める()
        return self.今回の行動

    def 利得計算(self, 相手の行動: 行動, 今回の利得: 利得):
        self.利得 += 今回の利得
        self._次の行動に備える(相手の行動, 今回の利得)

    @abstractmethod
    def _行動を決める(self) -> 行動:
        pass

    @abstractmethod
    def _次の行動に備える(self, 相手の行動: 行動, 今回の利得: 利得):
        pass


class ランダムに行動する囚人(囚人):
    def _行動を決める(self) -> 行動:
        if (random() < 0.5):
            return 行動.自白

        return 行動.黙秘

    def _次の行動に備える(self, 相手の行動: 行動, 今回の利得: 利得):
        pass


class 日和見する囚人(囚人):
    def _行動を決める(self) -> 行動:
        return 行動.黙秘

    def _次の行動に備える(self, 相手の行動: 行動, 今回の利得: 利得):
        pass


class 裏切り続ける囚人(囚人):
    def _行動を決める(self) -> 行動:
        return 行動.自白

    def _次の行動に備える(self, 相手の行動: 行動, 今回の利得: 利得):
        pass


class しっぺ返しする囚人(囚人):
    def __init__(self) -> None:
        super().__init__()
        self.相手の前回の行動 = None
        self.裏切られた = False

    def _行動を決める(self) -> 行動:
        if not self.裏切られた:
            return 行動.黙秘

        assert self.相手の前回の行動 is not None

        return self.相手の前回の行動

    def _次の行動に備える(self, 相手の行動: 行動, 今回の利得: 利得):
        if not self.裏切られた:
            if 相手の行動 == 行動.自白:
                self.裏切られた = True

        self.相手の前回の行動 = 相手の行動


class シミュレータ:
    def __init__(self, 囚人1: 囚人, 囚人2: 囚人) -> None:
        self.囚人1 = 囚人1
        self.囚人2 = 囚人2
        self.利得計算器 = 利得()

    def シミュレート(self, n_iter: int):
        for _ in range(n_iter):
            self._行動()

        print(f'囚人1: {self.囚人1.利得}')
        print(f'囚人2: {self.囚人2.利得}')

    def _行動(self):
        行動1 = self.囚人1.行動()
        行動2 = self.囚人2.行動()

        # print(f'{行動1} : {行動2}')

        利益1, 利益2 = self.利得計算器.計算(行動1, 行動2)

        self.囚人1.利得計算(行動2, 利益1)
        self.囚人2.利得計算(行動1, 利益2)


if __name__ == '__main__':
    for other in [ランダムに行動する囚人(), 日和見する囚人(), 裏切り続ける囚人()]:
        s = シミュレータ(しっぺ返しする囚人(), other)
        s.シミュレート(1000)
