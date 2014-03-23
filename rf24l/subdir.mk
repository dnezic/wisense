
# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../RF24.cpp \
../compatibility.cpp \
../gpio.cpp \
../spi.cpp 

OBJS += \
./RF24.o \
./compatibility.o \
./gpio.o \
./spi.o 

CPP_DEPS += \
./RF24.d \
./compatibility.d \
./gpio.d \
./spi.d 


# Each subdirectory must supply rules for building sources it contributes
%.o: ../%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -mfpu=vfp -mfloat-abi=hard -march=armv6zk -mtune=arm1176jzf-s -O3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<" -fPIC
	@echo 'Finished building: $<'
	@echo ' '



