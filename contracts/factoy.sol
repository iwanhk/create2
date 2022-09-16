// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

// 创建合约时，合约的地址是根据创建合约的地址和随着每次合约创建而增加的计数器计算出来的。

// 如果您指定选项salt（bytes32 值），则合约创建将使用不同的机制来提供新合约的地址：

// 它将根据创建合约的地址、给定的盐值、创建合约的（创建）字节码和构造函数参数来计算地址。

contract Factory {
    address public lastDeployed;

    // 返回新部署的合约地址
    function Deploy(string memory _salt) public payable {
        // 此语法是一种无需组装即可调用 create2 的较新方法，您只需要传递 salt
        // https://docs.soliditylang.org/en/latest/control-structures.html#salted-contract-creations-create2
        lastDeployed = address(
            new TestContract{salt: bytes32(abi.encode(_salt))}(msg.sender, 255)
        );
    }
}

// 这是使用汇编的旧方法
contract FactoryAssembly {
    event Deployed(address addr, uint256 salt);
    struct Record {
        address addr;
        uint256 salt;
    }
    Record[] public deployRecords;

    // 1. 获取要部署的合约字节码
    // 注意：_owner 和 _foo 是 TestContract 构造函数的参数
    function getBytecode(address owner, uint256 foo)
        public
        pure
        returns (bytes memory)
    {
        bytes memory bytecode = type(TestContract).creationCode;

        return abi.encodePacked(bytecode, abi.encode(owner, foo));
    }

    // 2. 计算要部署的合约地址
    // 注意：_salt 是用于创建地址的随机数
    function getAddress(bytes memory bytecode, uint256 _salt)
        public
        view
        returns (address)
    {
        bytes32 hash = keccak256(
            abi.encodePacked(
                bytes1(0xff),
                address(this),
                _salt,
                keccak256(bytecode)
            )
        );

        // 注意：将最后 20 个字节的哈希值转换为地址
        return address(uint160(uint256(hash)));
    }

    // 3. 部署合约
    // 注意：
    // 检查事件日志 Deployed，其中包含已部署的 TestContract 的地址。
    // 日志中的地址应该等于从上面计算的地址。
    function Deploy(bytes memory bytecode, uint256 _salt) external {
        address addr;

        /*
        注意: 如何调用 create2 ? 

        create2(v, p, n, s)
        使用内存 p 到 p + n 的代码创建新合约
        并发送 v wei
        并返回新地址
        where new address = 前 20 bytes of keccak256(0xff + address(this) + s + keccak256(mem[p…(p+n)))
              s = big-endian 256-bit value
        */
        assembly {
            addr := create2(
                callvalue(), // wei sent with current call
                // Actual code starts after skipping the first 32 bytes
                add(bytecode, 0x20),
                mload(bytecode), // Load the size of code contained in the first 32 bytes
                _salt // Salt from function arguments
            )

            if iszero(extcodesize(addr)) {
                revert(0, 0)
            }
        }

        emit Deployed(addr, _salt);
        deployRecords.push(Record(addr, _salt));
    }
}

contract TestContract {
    address public owner;
    uint256 public foo;

    constructor(address _onwer, uint256 _foo) {
        owner = _onwer;
        foo = _foo;
    }
}
