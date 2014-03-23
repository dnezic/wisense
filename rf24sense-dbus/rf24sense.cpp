/*
 * starter.cpp
 *
 * Copyright 2014, Drazen Nezic, www.svesoftware.com
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *   http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 *  Created on: Mar 22, 2014
 *      Author: dnezic
 */

#include <stdio.h>
#include <stdlib.h>
#include <cstdlib>
#include <iostream>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#include <RF24.h>
#include <dbus_sender.h>
#include "rf24sense.h"

/* CE pin is number 25. */
RF24 radio(SPI_DEV, 8000000, RPI_CE_PIN);

/* Radio pipe addresses for the 2 nodes to communicate. */
const uint64_t pipes[2] = { 0x7365727631LL, 0xF0F0F0F0E3LL };

/* log writing for debugging */
FILE* destFile;

bool debug = false;

#define DBUS_SENDER "wisense"
#define DBUS_OBJECT "/com/svesoftware/raspberry/lcd"
#define DBUS_INTERFACE "com.svesoftware.raspberry.lcd"
#define DBUS_TARGET "com.svesoftware.raspberry.lcd"
#define DBUS_METHOD "draw"

void setup(void) {
	radio.setPayloadSize(PAYLOAD_SIZE);
	radio.begin();
	/* no dynamic payloads */
	// radio.enableDynamicPayloads();
	/* manual ACK control */
	radio.setAutoAck(0);

	/* maximum range */
	radio.setDataRate(RF24_250KBPS);
	radio.setPALevel(RF24_PA_MAX);

	radio.setChannel(0x50);
	radio.setCRCLength(RF24_CRC_16);

	radio.openWritingPipe(pipes[1]);
	radio.openReadingPipe(1, pipes[0]);

	//
	// Start listening
	//

	radio.startListening();

	//
	// Dump the configuration of the rf unit for debugging
	//
	radio.printDetails();

}

void loop(void) {

	int i = 0;

	/* wait some to release CPU */
	delay(20);

	if (radio.available()) {

		unsigned char payload_buffer[PAYLOAD_SIZE];
		bool done = false;

		while (!done) {
			done = radio.read(&payload_buffer[0], PAYLOAD_SIZE);
			if (done) {
				printf("Debug: ");
				for (i = 0; i < PAYLOAD_SIZE; i++) {
					printf("%d ", payload_buffer[i]);
				}
				printf("\n");

				int voltage = 0;
				voltage = voltage | payload_buffer[0];
				voltage = voltage << 8;
				voltage = voltage | payload_buffer[1];

				printf("Voltage: %d (mV)\n", voltage);
				printf("Humidity: %d.%d\n", (int) payload_buffer[2], (int) payload_buffer[3]);
				printf("Temperature: %d.%d\n", (int) payload_buffer[4], (int) payload_buffer[5]);
				printf("EC: %d\n", (int) payload_buffer[6]);
				printf("Counter: %d\n", (int) payload_buffer[7]);

				char lcd[32];
				char timestr[10];

				time_t now = time(NULL);
				struct tm *t = localtime(&now);
				strftime(timestr, sizeof(timestr) - 1, "%H:%M", t);

				sprintf(lcd, "%s  %d (mV) %d.%dC %d.%d%%", timestr, voltage, (int) payload_buffer[4], (int) payload_buffer[5], (int) payload_buffer[2], (int) payload_buffer[3]);

				if (debug) {
					destFile = fopen(LOG_FILE, "a");
					fprintf(destFile, "%s  %d (mV) %d.%dC %d.%d%% EC: %d CNT: %d\n", timestr, voltage, (int) payload_buffer[4], (int) payload_buffer[5], (int) payload_buffer[2],
							(int) payload_buffer[3], (int) payload_buffer[6], (int) payload_buffer[7]);
					fclose(destFile);
				}

				/* send bus signal */
				sendsignal(DBUS_SENDER, lcd, DBUS_TARGET, DBUS_OBJECT, DBUS_INTERFACE, DBUS_METHOD);

			}

		}

	}

}

int main(int argc, char** argv) {

	printf("rf24sense - data receiver from nrf24l01p device.\n");

	if (argc > 1) {
		if (strcmp(argv[1], "-v") == 0) {
			debug = true;
		}
		if (strcmp(argv[1], "-h") == 0) {
			printf("Usage: ./rf24sense [-v]\n-v write data to data.log file.\n");
		}
	}

	setup();
	while (1)
		loop();

	return 0;
}
