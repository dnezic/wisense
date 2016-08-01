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
#include <zmq.h>
#include <assert.h>

#include <RF24.h>
#include "rf24sense.h"

RF24 radio(RPI_GPIO_P1_22, RPI_GPIO_P1_24, BCM2835_SPI_SPEED_8MHZ);

/* Radio pipe addresses for the 2 nodes to communicate. */
const uint64_t pipes[2] = { 0x7365727631LL, 0xF0F0F0F0E3LL };

/* log writing for debugging */
FILE* destFile;

bool debug = false;


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

	radio.startListening();

	//
	// Dump the configuration of the rf unit for debugging
	//
	radio.printDetails();

}


void my_free (void *data, void *hint)
{
    free (data);
}

void loop(void) {

	int i = 0;

	/* wait some to release CPU */
	delay(20);

	if (radio.available()) {

		unsigned char payload_buffer[PAYLOAD_SIZE];
		bool done = false;

		radio.read(&payload_buffer[0], PAYLOAD_SIZE);
		for (i = 0; i < PAYLOAD_SIZE; i++) {
			printf("%d ", payload_buffer[i]);
		}
		printf("\n");

		int voltage = 0;
		voltage = voltage | payload_buffer[0];
		voltage = voltage << 8;
		voltage = voltage | payload_buffer[1];

		printf("Voltage: %d (mV)\n", voltage);
		printf("Temperature: %d.%d\n", (int) payload_buffer[2], (int) payload_buffer[3]);

		int8_t temperature = (int8_t) payload_buffer[2];
		int8_t temperature_dec = (int8_t) payload_buffer[3];

		long pressure = (int) payload_buffer[5];
		pressure = pressure << 8;
		pressure = pressure | (int) payload_buffer[4];
                float pressure_f = pressure + ((float) payload_buffer[6] / 100);
		int8_t humidity = (int8_t) payload_buffer[8];
		printf("Pressure: %f\n", pressure_f);
		printf("Counter: %d\n", (int) payload_buffer[13]);
		printf("Error count: %d\n", (int) payload_buffer[14]);
                                
                int counter = (int) payload_buffer[13];
                int i2c_error_count = (int) payload_buffer[14];

		char lcd[128];
//                char hub[128];
		char timestr[10];

		time_t now = time(NULL);
                float temperature_f = temperature + (temperature_dec/100.0);
		sprintf(lcd, "NRF24%.1f:%d%:%.1f", temperature_f, humidity, pressure_f);
                // sprintf(lcd, "%-20s", lcd);
                /* send data to the LCD */
                long linger = 1000;
                void *context = zmq_init(1);
                void *sender = zmq_socket (context, ZMQ_REQ);
                zmq_setsockopt(sender, ZMQ_LINGER, &linger, sizeof(linger));
	        int rc = zmq_connect (sender, "tcp://localhost:6000");
                void *data = malloc (20);
                assert(data);
                memcpy (data, lcd, 20);
                zmq_msg_t msg;
                rc = zmq_msg_init_data (&msg, data, 20, my_free, NULL);
                assert(rc == 0);
                                
                zmq_send (sender, &msg, 1);
                zmq_close (sender);
                zmq_term(context);        
        
		if (debug) {
			destFile = fopen(LOG_FILE, "a");
			fprintf(destFile, "%s  %d (mV) %d.%dC %.2f %d.%dC %d.%d%% CNT: %d %d %d\n", timestr, voltage, temperature, temperature_dec, pressure_f, (int) payload_buffer[8], (int) payload_buffer[9], (int) payload_buffer[10], (int) payload_buffer[11], (int) payload_buffer[12], (int)payload_buffer[13], (int)payload_buffer[14]);
			fclose(destFile);
		}
	}

}



int main(int argc, char** argv) {

	printf("rf24sense - data receiver from nrf24l01p device.\n");
        

	if (argc > 1) {
		if (strcmp(argv[1], "-v") == 0) {
			debug = true;
		}
		else if (strcmp(argv[1], "-h") == 0) {
			printf("Usage: ./rf24sense [-v]\n-v write data to data.log file.\n");
			return -1;
		}
		else {
			return -1;
		}
	}

	setup();
	while (1)
		loop();

	
        return 0;
}
