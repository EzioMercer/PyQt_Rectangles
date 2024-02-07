from typing import Literal


def sign(num: int) -> Literal[1, -1, 0]:
	if num > 0:
		return 1

	if num < 0:
		return -1

	return 0
