CXXFLAGS =	-O2 -g -Wall -mfpu=vfp -mfloat-abi=hard -march=armv6zk -mtune=arm1176jzf-s -fmessage-length=0 -L/usr/local/lib -I/usr/local/include/RF24

OBJS =		rf24sense.o

LIBS =		-lrf24-bcm -lzmq

TARGET =	rf24sense

$(TARGET):	$(OBJS)
	$(CXX) $(CXXFLAGS)  $(LIBS) -o $(TARGET) $(OBJS)

all:	$(TARGET)

clean:
	rm -f $(OBJS) $(TARGET)
