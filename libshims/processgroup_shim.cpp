/*
 * SPDX-FileCopyrightText: The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

#include <processgroup/processgroup.h>

#include <string>
#include <vector>

// Stock libcameraopt.so imports SetTaskProfiles with C linkage.
extern "C" bool SetTaskProfilesC(int tid, const std::vector<std::string>& profiles,
                                 bool use_fd_cache) __asm__("SetTaskProfiles");

extern "C" bool SetTaskProfilesC(int tid, const std::vector<std::string>& profiles,
                                 bool use_fd_cache) {
    return SetTaskProfiles(tid, profiles, use_fd_cache);
}
