import React, {useEffect, useState} from 'react'
import {Nav,Container, Table, Button, Modal, Row, Form, Col, Alert} from 'react-bootstrap';
import store from 'store-js';
import Router from 'next/router';
import UsersServices from '../../https/users';
import LoaderComponent from '../../components/LoaderComponent';
import NavComponent from '../../components/NavComponent';

const home = () => {
  const user = store.get('user');
  const [loading, setLoading] = useState(false);
  const [reload, setReload] = useState(false);
  const [usersList, setUsersList] = useState([]);
  const [show, setShow] = useState(false);
  const [showEdit, setShowEdit] = useState(false);

  const [error, setError] = useState(false);
  const [msgError, setMsgError] = useState('');

  const [username, setUserName] = useState('');
  const [pk, setPk] = useState();
  const [firtsName, setFirtsName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [isAdmin, setIsAdmin] = useState(false);
  const [isManager, setIsManager] = useState(false);

  async function createHandleSubmit(event) {
    setLoading(true)
    event.preventDefault();
    const body = {
        username: username,
        first_name: firtsName,
        last_name: lastName,
        email: email,
        phone_number: phone,
        is_manager: isManager,
        is_superuser: isAdmin,
        is_staff: isAdmin
    }
    UsersServices.user_create(user.access, body)
    .then(() =>{
      setLoading(false)
      setShow(false)
      setReload(!reload)

    })
    .catch( err =>{
      setShow(false)
      setError(true)
      setMsgError(JSON.stringify(err))
      setLoading(false)
    })
  }

  async function editHandleSubmit(event){
    setLoading(true)
    setShowEdit(false)
    event.preventDefault();
    const body = {
      pk,
      username: username,
      first_name: firtsName,
      last_name: lastName,
      email: email,
      phone_number: phone,
      is_manager: isManager,
      is_superuser: isAdmin,
      is_staff: isAdmin
  }
  UsersServices.user_edit(user.access, body)
  .then(() =>{
    setLoading(false)
    setReload(!reload)
  })
  .catch( err =>{
    setError(true)
    setMsgError(JSON.stringify(err))
    setLoading(false)
  })
  }

  async function OpenModalEditUser(userId) {
    UsersServices.user_detail(user.access, userId)
    .then(res => {
      setPk(res.data.pk)
      setUserName(res.data.username)
      setFirtsName(res.data.first_name)
      setLastName(res.data.last_name)
      setEmail(res.data.email)
      setPhone(res.data.phone_number)
      setIsAdmin(res.data.is_staff)
      setIsManager(res.data.is_manager)
      setShowEdit(true)
    })
  };

  async function DeleteUser(userId) {
    setLoading(true)
    UsersServices.user_delete(user.access, userId)
  .then(() =>{
    setLoading(false)
    setReload(!reload)
  })
  .catch( err =>{
    setError(true)
    setMsgError(JSON.stringify(err))
    setLoading(false)
  })

  };

  useEffect(() => {
    setUserName('')
    setFirtsName('')
    setLastName('')
    setEmail('')
    setPhone('')
    setIsAdmin(false)
    setIsManager(false)
    setLoading(true)
    setError(false)

    if(!user || !user.is_superuser || !user.is_staff){
      store.clearAll();
      Router.push('/');
    }
    UsersServices.user_list(user.access)
    .then(res => {
      setUsersList(res.data)
      setLoading(false)
    })
    .catch(() => {
      setLoading(false)
    })
	}, [reload]);


  return (
    <>
    <NavComponent user={user} />
    <Container>
    {loading ? <LoaderComponent/> :
      <>
      {error ? <Alert variant='danger'>
            {msgError}
          </Alert>: ''}
      <h3>Users of system</h3> <Button variant="primary" onClick={() => setShow(true)}>Add User</Button>
      <br/>
      <br/>
    <Table striped bordered hover>
      <thead>
        <tr>
          <th>#</th>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Username</th>
          <th>Email</th>
          <th>Phone</th>
          <th>Admin</th>
          <th>Manager</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>

        {
          usersList.map(user =>{
            return (
              <tr key={user.pk}>
                <td>{user.pk}</td>
                <td>{user.first_name}</td>
                <td>{user.last_name}</td>
                <td>{user.username}</td>
                <td>{user.email}</td>
                <td>{user.phone_number}</td>
                <td>{user.is_staff.toString()}</td>
                <td>{user.is_manager.toString()}</td>
                <td>
                <>
                  <Button variant="warning" onClick={() => {OpenModalEditUser(user.pk)}}>Edit</Button>{' '}
                  <Button variant="danger" onClick={()=> {DeleteUser(user.pk)}}>DEL</Button>
                </>
                </td>
              </tr>
            )
          })
        }
      </tbody>
    </Table>
    <Modal
        show={show}
        onHide={() => setShow(false)}
        dialogClassName="modal-90w"
        aria-labelledby="example-custom-modal-styling-title"
      >
        <Modal.Header closeButton>
          <Modal.Title id="example-custom-modal-styling-title">
            Add new User
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
        <Form onSubmit={createHandleSubmit}>
            <Form.Group controlId="formBasicusername">
              <Form.Label>Username</Form.Label>
              <Form.Control type="text" placeholder="Enter username"
              onChange={e => setUserName(e.target.value)}
                />
            </Form.Group>
            <Form.Group controlId="formBasicFirstName">
              <Form.Label>First Name</Form.Label>
              <Form.Control type="text" placeholder="Enter First Name"
              onChange={e => setFirtsName(e.target.value)}
                />
            </Form.Group>
            <Form.Group controlId="formBasicLastName">
              <Form.Label>Last Name</Form.Label>
              <Form.Control type="text" placeholder="Enter Last Name"
              onChange={e => setLastName(e.target.value)}
                />
            </Form.Group>
            <Form.Group controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control type="email" placeholder="Enter email"
              onChange={e => setEmail(e.target.value)}
                />
            </Form.Group>
            <Form.Group controlId="formBasicPhone">
              <Form.Label>Phone number</Form.Label>
              <Form.Control type="text" placeholder="Enter phone number"
              onChange={e => setPhone(e.target.value)}
                />
            </Form.Group>
            <Form.Group controlId="formBasicAdmin">
              <Form.Label>Permissions</Form.Label>
              <br/>
              <Form.Check
                  inline
                  label="Super Admin"
                  name="group1"
                  type="radio"
                  id='inline-radio-1'
                  onChange={() => {
                    setIsAdmin(true)
                    setIsManager(false)
                    }
                  }
                />
                <Form.Check
                  inline
                  label="Food Manager"
                  name="group1"
                  type="radio"
                  id='inline-radio-1'
                  onChange={() => {
                    setIsAdmin(false)
                    setIsManager(true)
                    }
                  }
                />
            </Form.Group>

            <br/>
            <Button variant="primary" type="submit" disabled={!username || !firtsName || !lastName || !email || !phone}>Create</Button>
          </Form>
        </Modal.Body>
      </Modal>
    <Modal
      show={showEdit}
      onHide={() => setShowEdit(false)}
      dialogClassName="modal-90w"
      aria-labelledby="example-custom-modal-styling-title"
    >
      <Modal.Header closeButton>
        <Modal.Title id="example-custom-modal-styling-title">
          Edit User
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
      <Form onSubmit={editHandleSubmit}>
          <Form.Group controlId="formBasicusername">
            <Form.Label>Username</Form.Label>
            <Form.Control type="text" placeholder="Enter username"
            value={username}
            onChange={e => setUserName(e.target.value)}
              />
          </Form.Group>
          <Form.Group controlId="formBasicFirstName">
            <Form.Label>First Name</Form.Label>
            <Form.Control type="text" placeholder="Enter First Name"
            value={firtsName}
            onChange={e => setFirtsName(e.target.value)}
              />
          </Form.Group>
          <Form.Group controlId="formBasicLastName">
            <Form.Label>Last Name</Form.Label>
            <Form.Control type="text" placeholder="Enter Last Name"
            value={lastName}
            onChange={e => setLastName(e.target.value)}
              />
          </Form.Group>
          <Form.Group controlId="formBasicEmail">
            <Form.Label>Email address</Form.Label>
            <Form.Control type="email" placeholder="Enter email"
            value={email}
            onChange={e => setEmail(e.target.value)}
              />
          </Form.Group>
          <Form.Group controlId="formBasicPhone">
            <Form.Label>Phone number</Form.Label>
            <Form.Control type="text" placeholder="Enter phone number"
            value={phone}
            onChange={e => setPhone(e.target.value)}
              />
          </Form.Group>
          <Form.Group controlId="formBasicAdmin">
            <Form.Label>Permissions</Form.Label>
            <br/>
            <Form.Check
                inline
                checked={isAdmin}
                label="Super Admin"
                name="group1"
                type="radio"
                id='inline-radio-1'
                onChange={() => {
                  setIsAdmin(true)
                  setIsManager(false)
                  }
                }
              />
              <Form.Check
                inline
                checked={isManager}
                label="Food Manager"
                name="group1"
                type="radio"
                id='inline-radio-1'
                onChange={() => {
                  setIsAdmin(false)
                  setIsManager(true)
                  }
                }
              />
          </Form.Group>

          <br/>
          <Button variant="primary" type="submit" disabled={!username || !firtsName || !lastName || !email || !phone}>Editar</Button>
        </Form>
      </Modal.Body>
    </Modal>
    </>
    }

    </Container>
    </>
  )
}

export default home
