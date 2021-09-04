pragma solidity ^0.8;

contract PrivateData{
    uint numberParents = 0;
    uint numberPatients = 0;
    struct Patient{
        uint256 id;
        string name;
        string familyName;
        string birthdate;
    }
    mapping(uint => Patient) public patients;

    function  createPatient(uint256 id, string memory name, string memory familyName, string memory birthdate) public{
        patients[id] = Patient(id, name, familyName, birthdate);
    }

    function getPatientById(uint256 id) public view returns(Patient memory){
        return patients[id];
    }

    function deletePatient(uint256 id) public {
        delete patients[id];
    }


    function updatePatient(uint256 id, string memory name, string memory familyName, string memory birthdate) public{
        Patient memory patient = getPatientById(id);
        patient.name = name;
        patient.familyName = familyName;
        patient.birthdate = birthdate;
        patients[id] = patient;
    }
}
