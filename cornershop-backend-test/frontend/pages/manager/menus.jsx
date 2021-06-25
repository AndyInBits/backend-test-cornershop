import React, {useEffect, useState} from 'react'
import {Nav,Container, Table, Button, Modal, Row, Form, Col, Alert,Select, FormControl} from 'react-bootstrap';
import LoaderComponent from '../../components/LoaderComponent';
import NavComponent from '../../components/NavComponent';
import store from 'store-js';
import MenuServices from '../../https/menus';
import Router from 'next/router';
import DropdownMultiselect from "react-multiselect-dropdown-bootstrap";


const menus = () => {
  const user = store.get('user');
  const [loading, setLoading] = useState(false);
  const [reload, setReload] = useState(false);
  const [menusList, setMenusList] = useState([]);
  const [optionsList, setOptionsList] = useState([]);
  const [selectOptionsList, setSelectOptionsList] = useState([]);
  const [selectOptionsListDetail, setSelectOptionsListDetail] = useState([]);
  const [error, setError] = useState(false);
  const [msgError, setMsgError] = useState('');

  const [showOptions, setShowOptions] = useState(false);
  const [optionName, setOptionName] = useState('');
  const [show, setShow] = useState(false);
  const [showEdit, setShowEdit] = useState(false);

  const [pk, setPk] = useState();
  const [name, setName] = useState('');
  const [reminder, setReminder] = useState(false);
  const [available, setAvailable] = useState(false);
  const [date, setDate] = useState('');

  async function createOptionHandleSubmit(event){
    setLoading(true)
    event.preventDefault();
    const body = {
      option: optionName
    }
    MenuServices.menu_option_create(user.access, body)
    .then(() =>{
      setLoading(false)
      setShowOptions(false)
      setReload(!reload)

    })
    .catch( err =>{
      setShowOptions(false)
      setError(true)
      setMsgError(JSON.stringify(err))
      setLoading(false)
    })
  }
  async function createHandleSubmit(event) {
    setLoading(true)
    event.preventDefault();
    const body = {
      name,
      reminder,
      available,
      date,
      options: selectOptionsList.map(id => {
        return parseInt(id)
      })
    }
    MenuServices.menu_create(user.access, body)
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

  async function DeleteMenu(menuId) {
    setLoading(true)
    MenuServices.menu_delete(user.access, menuId)
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
    setError(false)
    setMsgError('')
    setPk('')
    setName('')
    setReminder('')
    setAvailable('')
    setDate('')
    setSelectOptionsListDetail([])
    setLoading(true);
    if(!user || !user.is_manager){
      store.clearAll();
      Router.push('/');
    }
    MenuServices.menu_option_list(user.access)
    .then(res => {
      setOptionsList(res.data.map(opt => {
        return {key: opt.pk, label: opt.option}
      }));
    })
    .catch(() => {
      setLoading(false)
    })
    MenuServices.menu_list(user.access)
    .then(res => {
      setMenusList(res.data)
      setLoading(false)
    })
    .catch(() => {
      setLoading(false)
    })

  }, [reload]);

  async function OpenModalEditMenu(menuId) {
    MenuServices.menu_detail(user.access, menuId)
    .then(res => {
      setPk(res.data.pk)
      setName(res.data.name)
      setReminder(res.data.reminder)
      setAvailable(res.data.available)
      setDate(res.data.date)
      setSelectOptionsListDetail(res.data.options)
      setShowEdit(true)
    })
  };

  async function editHandleSubmit(event){
    setLoading(true)
    setShowEdit(false)
    event.preventDefault();

    const body = {
      pk,
      name,
      reminder,
      available,
      date,
      options: selectOptionsList.map(id => {
        return parseInt(id)
      })
    }
    MenuServices.menu_edit(user.access, body)
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
  return (
    <>
      <NavComponent user={user}/>
      <Container>
        {loading ? <LoaderComponent/> : <>
          {error ? <Alert variant='danger'>
            {msgError}
          </Alert>: ''}
          <h3>Handlers Menus</h3>
          <Button variant="primary" onClick={() => setShow(true)}>Add Menu</Button>{' '}
          <Button variant="primary" onClick={() => setShowOptions(true)}>Add Menu Options</Button>
          <br/>
          <br/>
      <Table striped bordered hover>
      <thead>
        <tr>
          <th>#</th>
          <th>Menu</th>
          <th>Date</th>
          <th>Reminder</th>
          <th>Available</th>
          <th>Options</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>

        {
          menusList.map(menu =>{
            return (
              <tr key={menu.pk}>
                <td>{menu.pk}</td>
                <td>{menu.name}</td>
                <td>{menu.date}</td>
                <td>{menu.reminder.toString()}</td>
                <td>{menu.available.toString()}</td>
                <td>
                <ul>
                {menu.options.map( opt => {
                  return (
                  <li key={opt.pk}>
                    {opt.option}
                  </li>)
                })}
                </ul>
                </td>
                <td>
                <>
                  <Button variant="warning" onClick={()=> {OpenModalEditMenu(menu.pk)}}>Edit</Button>{' '}
                  <Button variant="danger" onClick={()=> {DeleteMenu(menu.pk)}}>DEL</Button>
                </>
                </td>
              </tr>
            )
          })
        }
      </tbody>
    </Table>
        </>}
        <Modal
        show={show}
        onHide={() => setShow(false)}
        dialogClassName="modal-90w"
        aria-labelledby="example-custom-modal-styling-title"
      >
        <Modal.Header closeButton>
          <Modal.Title id="example-custom-modal-styling-title">
            Add new Menu
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
        <Form onSubmit={createHandleSubmit}>
            <Form.Group controlId="formBasicmenuName">
              <Form.Label>Name</Form.Label>
              <Form.Control type="text" placeholder="Enter name menu"
                onChange={e => setName(e.target.value)}
              />
            </Form.Group>
            <br/>
            <Form.Group controlId="formBasicCheckbox">
              <Form.Check type="checkbox" label="Active reminder" onChange={e => setReminder(!reminder)}/>
            </Form.Group>
            <Form.Group controlId="formBasicCheckbox">
              <Form.Check type="checkbox" label="	Available" onChange={e => setAvailable(!available)}/>
            </Form.Group>
            <br/>
            <Form.Group controlId="dob">
                  <Form.Label>Select Date</Form.Label>
                  <Form.Control type="date" placeholder="Date of Birth"
                    onChange={e => setDate(e.target.value)}
                  />
              </Form.Group>
              <br/>
              <Form.Group controlId="exampleForm.SelectCustom">
                <DropdownMultiselect options={optionsList} name="options"
                  handleOnChange={(selected) => setSelectOptionsList(selected)}
                />
              </Form.Group>
            <br/>
            <br/>
            <Button variant="primary" type="submit" disabled={!name || !date }>Create</Button>
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
            Edit Menu
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
        <Form onSubmit={editHandleSubmit}>
            <Form.Group controlId="formBasicmenuName">
              <Form.Label>Name</Form.Label>
              <Form.Control type="text" placeholder="Enter name menu"
              value={name}
              onChange={e => setName(e.target.value)}
              />
            </Form.Group>
            <br/>
            <Form.Group controlId="formBasicCheckbox">
              <Form.Check type="checkbox" label="Active reminder" onChange={e => setReminder(!reminder)}
              checked={reminder}
              />
            </Form.Group>
            <Form.Group controlId="formBasicCheckbox">
              <Form.Check type="checkbox" label="	Available" onChange={e => setAvailable(!available)}
                checked={available}
              />
            </Form.Group>
            <br/>
            <Form.Group controlId="dob">
                  <Form.Label>Select Date</Form.Label>
                  <Form.Control type="date" placeholder="Date of Birth"
                    onChange={e => setDate(e.target.value)}
                    value={date}
                  />
              </Form.Group>
              <br/>
              <Form.Group controlId="exampleForm.SelectCustom">
                <DropdownMultiselect options={optionsList} name="options"
                  handleOnChange={(selected) => setSelectOptionsList(selected)}
                  selected={selectOptionsListDetail.map(opt => {
                    return opt.pk.toString()
                  })}
                />
              </Form.Group>
            <br/>
            <br/>
            <Button variant="primary" type="submit" disabled={!name || !date }>Edit</Button>
          </Form>
        </Modal.Body>
      </Modal>
      <Modal
        show={showOptions}
        onHide={() => setShowOptions(false)}
        dialogClassName="modal-90w"
        aria-labelledby="example-custom-modal-styling-title"
      >
        <Modal.Header closeButton>
          <Modal.Title id="example-custom-modal-styling-title">
            Add Option Menu
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
        <Form onSubmit={createOptionHandleSubmit}>
            <Form.Group controlId="formBasicmenuName">
              <Form.Label>Name Option</Form.Label>
              <Form.Control type="text" placeholder="Enter name option"
              onChange={e => setOptionName(e.target.value)}
              />
            </Form.Group>
            <br/>
            <br/>
            <Button variant="primary" type="submit" disabled={!optionName}>create</Button>
          </Form>
        </Modal.Body>
      </Modal>
      </Container>
    </>
  )
}

export default menus
