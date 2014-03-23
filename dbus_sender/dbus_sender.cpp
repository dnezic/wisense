/*
 * dbus_sender.cpp
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

#include <stdbool.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <dbus/dbus.h>
#include "dbus_sender.h"

/**
 * Connect to the DBUS bus and send a broadcast signal
 *
 * example:
 *
 * sendsignal("sender", "com.svesoftware.raspberry.lcd", "/com/svesoftware/raspberry/lcd", "com.svesoftware.raspberry.lcd", "draw");
 *
 */
int sendsignal(const char* sender, char* sigvalue, const char* target, const char* object, const char *interface, const char *method_name) {
	DBusMessage* msg;
	DBusMessageIter args;
	DBusConnection* conn;
	DBusError err;

	dbus_uint32_t serial = 0;

	// initialise the error value
	dbus_error_init(&err);

	// connect to the DBUS system bus, and check for errors
	conn = dbus_bus_get(DBUS_BUS_SYSTEM, &err);
	if (dbus_error_is_set(&err)) {
		fprintf(stderr, "Connection Error (%s)\n", err.message);
		dbus_error_free(&err);
		return -1;
	}
	if (NULL == conn) {
		return -2;
	}

	msg = dbus_message_new_method_call(target, // target for the method call
			object, // object to call on
			interface, // interface to call on
			method_name); // method name

	if (NULL == msg) {
		fprintf(stderr, "Message Null\n");
		exit(1);
	}

	// append arguments onto signal
	dbus_message_iter_init_append(msg, &args);
	if (!dbus_message_iter_append_basic(&args, DBUS_TYPE_STRING, &sigvalue)) {
		fprintf(stderr, "Out Of Memory!\n");
		return -3;
	}
	if (!dbus_message_iter_append_basic(&args, DBUS_TYPE_STRING, &sender)) {
		fprintf(stderr, "Out Of Memory!\n");
		return -4;
	}
	if (!dbus_message_iter_append_basic(&args, DBUS_TYPE_STRING, &sigvalue)) {
		fprintf(stderr, "Out Of Memory!\n");
		return -5;
	}

	// send the message and flush the connection
	if (!dbus_connection_send(conn, msg, &serial)) {
		fprintf(stderr, "Out Of Memory!\n");
		return -6;
	}
	dbus_connection_flush(conn);
	// free the message
	dbus_message_unref(msg);
	return 0;
}

