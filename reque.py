import os
import json

class HealthCheck:
    def __init__(self):
        self._ids_file = "listin.txt"
        self._id_mapping = self.load_ids() # This will now store IDs as an attribute of the instance.
        self._checkup = None
        self._pulse = None
        self._alcot = None
        self._narcot = None
        self._zhaloby = None
        self._press = None
        self._temp = None
        self._receivedTouchID = None
        self._iin = None

    # Getter and Setter for checkup
    @property
    def checkup(self):
        return self._checkup

    @checkup.setter
    def checkup(self, value):
        self._checkup = value

    # Getter and Setter for pulse
    @property
    def pulse(self):
        return self._pulse

    @pulse.setter
    def pulse(self, value):
        self._pulse = value

    @property
    def receivedTouchID(self):
        return self._receivedTouchID

    @receivedTouchID.setter
    def receivedTouchID(self, value):
        self._receivedTouchID = value

    # Getter and Setter for alcot
    @property
    def alcot(self):
        return self._alcot

    @alcot.setter
    def alcot(self, value):
        self._alcot = value

    # Getter and Setter for narcot
    @property
    def narcot(self):
        return self._narcot

    @narcot.setter
    def narcot(self, value):
        self._narcot = value

    # Getter and Setter for zhaloby
    @property
    def zhaloby(self):
        return self._zhaloby

    @zhaloby.setter
    def zhaloby(self, value):
        self._zhaloby = value

    # Getter and Setter for press
    @property
    def press(self):
        return self._press

    @press.setter
    def press(self, value):
        self._press = value

    # Getter and Setter for temp
    @property
    def temp(self):
        return self._temp

    @temp.setter
    def temp(self, value):
        self._temp = value

    @property
    def iin(self):
        return self._iin

    @iin.setter
    def iin(self, value):
        self._iin = value


    def load_ids(self):
        if os.path.exists(self._ids_file):
            with open(self._ids_file, "r") as file:
                data = json.load(file)
                print(f"Loaded IDs: {data}")
                return data
        else:
            default_data = {1: "011215551090"}
            self._id_mapping = default_data
            self.save
    def save_ids(self):
        with open(self._ids_file, "w") as file:
            json.dump(self._id_mapping, file)
        print(f"Saved IDs: {self._id_mapping}")

    def addID(self, new_id):
        if not self._id_mapping:
            next_key = 1
        else:
            next_key = max(map(int, self._id_mapping.keys()), default=0) + 1
        self._id_mapping[str(next_key)] = new_id
        self.save_ids()

    def getLastRecordedID(self):
        if self._id_mapping:
            max_key = max(map(int, self._id_mapping.keys()), default=0)
            last_id = self._id_mapping[str(max_key)]
            print(f"Last Recorded ID: {last_id}")
            return last_id
        else:
            return None

    def getLastRecordedIDKey(self):
        if self._id_mapping:
            max_key = max(map(int, self._id_mapping.keys()), default=0)
            print(f"Last Recorded ID KEY : {max_key}")
            return max_key

        else:
            return None

    def getIDByKey(self, key):
        if key in self._id_mapping:
            return self._id_mapping[key]
        else:
            print(f"No ID found for key {key}")
            return None

    def reset_values(self):
        # Resetting numerical values to 0 or None for string/ID fields
        self._checkup = 0  # Assuming checkup can be represented with a numeric value
        self._pulse = 0
        self._alcot = 0
        self._narcot = 0
        self._zhaloby = None  # Assuming zhaloby is a string or similar
        self._press = 0
        self._temp = 0  # Assuming temp is a float
        self._receivedTouchID = None
        self._iin = None


