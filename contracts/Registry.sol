// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

contract Registry {
    struct DataType {
        bytes data;
        address owner;
    }
    mapping(string => DataType) public database;

    function store(string calldata _id, bytes calldata _data) external {
        DataType storage item = database[_id];

        require(
            item.owner == address(0) || item.owner == msg.sender,
            "Id used by others"
        );
        if (_data.length == 0) {
            // clean the database item
            delete database[_id];
            return;
        }
        if (item.owner == address(0)) {
            database[_id] = DataType(_data, msg.sender);
        } else {
            item.data = _data;
        }
    }

    function get(string calldata _id) external view returns (string memory) {
        return string(database[_id].data);
    }
}
