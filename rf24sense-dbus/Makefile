CXXFLAGS =	-O2 -g -Wall -mfpu=vfp -mfloat-abi=hard -march=armv6zk -mtune=arm1176jzf-s -fmessage-length=0 -L../rf24l/ -I../rf24l/ -L../dbus_sender/ -I../dbus_sender/ 

OBJS =		rf24sense.o

LIBS =		-lrf24l -ldbus_sender -ldbus-1

TARGET =	rf24sense

$(TARGET):	$(OBJS)
	$(CXX) $(CXXFLAGS)  $(LIBS) -o $(TARGET) $(OBJS)

all:	$(TARGET)

clean:
	rm -f $(OBJS) $(TARGET)
