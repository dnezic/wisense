# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../dbus_sender.cpp 

OBJS += \
./dbus_sender.o 

CPP_DEPS += \
./dbus_sender.d 


# Each subdirectory must supply rules for building sources it contributes

%.o: %.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++  -O3 -Wall -c -fmessage-length=0 -MMD -ldbus-1 -L/usr/lib/arm-linux-gnueabihf/ -I/usr/include/dbus-1.0 -I/usr/lib/arm-linux-gnueabihf/dbus-1.0/include -I. -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '



