CXXFLAGS =	-O2 -g -Wall -fmessage-length=0 -L../rf24l/Release -I../rf24l/ -I../dbus_sender/

OBJS =		rf24sense.o

LIBS =		-lrf24l

TARGET =	rf24sense

$(TARGET):	$(OBJS)
	$(CXX) $(CXXFLAGS)  $(LIBS) -o $(TARGET) $(OBJS)

all:	$(TARGET)

clean:
	rm -f $(OBJS) $(TARGET)
