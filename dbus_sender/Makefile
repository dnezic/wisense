
RM := rm -rf

-include subdir.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C++_DEPS)),)
-include $(C++_DEPS)
endif
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
ifneq ($(strip $(CC_DEPS)),)
-include $(CC_DEPS)
endif
ifneq ($(strip $(CPP_DEPS)),)
-include $(CPP_DEPS)
endif
ifneq ($(strip $(CXX_DEPS)),)
-include $(CXX_DEPS)
endif
ifneq ($(strip $(C_UPPER_DEPS)),)
-include $(C_UPPER_DEPS)
endif
endif


# Add inputs and outputs from these tool invocations to the build variables 

# All Target
all: libdbus_sender.so

# Tool invocations
libdbus_sender.so: $(OBJS) $(USER_OBJS)
	@echo 'Building target: $@'
	@echo 'Invoking: GCC C++ Linker'
	g++ -shared -mfpu=vfp -mfloat-abi=hard -march=armv6zk -mtune=arm1176jzf-s -o "libdbus_sender.so" $(OBJS) $(USER_OBJS) $(LIBS) -fPIC
	@echo 'Finished building target: $@'


# Other Targets
clean:
	-$(RM) $(OBJS)$(C++_DEPS)$(C_DEPS)$(CC_DEPS)$(ARCHIVES)$(CPP_DEPS)$(CXX_DEPS)$(C_UPPER_DEPS) libdbus_sender.so
	-@echo ' '

install:
	cp libdbus_sender.so /usr/lib/

.PHONY: all clean dependents
.SECONDARY:


