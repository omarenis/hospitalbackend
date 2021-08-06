pragma solidity ^0.6.0;

contract PrivateData{
    uint numberParents = 0;
    uint numberPatients = 0;
    struct Patient{
        uint id;
        string name;
        string familyName;
        string birthdate;
    }
    struct Parent{
        address id;
        string name;
        string familyName;
        string email;
        string telephone;
        string password;
        uint numberPatients;
        mapping(uint => uint) patients;
    }
    mapping(address => uint) parents;

    function public getParent(address _id) view returns (Parent){
        for(uint i=0; i < numberParents; i++){
            if(parents[i].id == _id){
                return parents[i];
            }
        }
        return null;
    }

    function public createParent(struct Parent memory parent){
        parents[numberParents] = parent;
        numberParents++;
    }
    constructor public(){

    }
}
