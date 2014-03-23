/*
 * dbus_sender.h
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

#ifndef DBUS_SENDER_H_
#define DBUS_SENDER_H_

extern int sendsignal(const char* sender, char* sigvalue, const char* target, const char* object, const char *interface, const char *method_name);


#endif /* DBUS_SENDER_H_ */
