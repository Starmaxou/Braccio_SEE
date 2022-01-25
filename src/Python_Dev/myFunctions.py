"""
 Map a value given from degree to a position for the motors
 @param value Value in degree
 @param startMin Min value at the beginning
 @param startMax Min value at the beginning
 @param stopMin Min value at the end
 @param stopMax Min value at the end
 @returns The value mapped
 """
def mapping(valueDegree, startMin, startMax, stopMin, stopMax) -> int :

	if valueDegree < startMin : valueDegree = startMin
	if valueDegree > startMax : valueDegree = startMax

	return int((valueDegree - startMin) * (stopMax - stopMin) / (startMax - startMin) + stopMin)
