#!/usr/bin/env python3

# Copyright (c) 2022 Seagate Technology LLC and/or its Affiliates

# This program is free software: you can redistribute it and/or modify it
# under the terms of the Apache-2.0 license as published by
# the Apache Software Foundation, either version 2.0 of the License,
# or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the License for the specific language governing permissions and
# limitations under the License.

# You should have received a copy of the Apache-2.0 license
# along with this program. If not, see <https://www.apache.org/licenses/LICENSE-2.0>.
# For any questions about this software or licensing, please email
# opensource@seagate.com

from enum import Enum


class RequestType(Enum):
    API = "a"
    REST = "r"


class EncodingType(Enum):
    BASE64 = "b"
    SHA256 = "s"
    BASE64_SHA256 = "bs"
