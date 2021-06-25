import React, { useState, useContext } from "react";
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Router from 'next/router';
import Row from 'react-bootstrap/Row';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Alert from 'react-bootstrap/Alert';
import AuthServices from '../https/auth';
import LoaderComponent from './LoaderComponent';
import store from 'store-js';

export const IndexComponent = () => {
  // const [, setUserContext] = useContext(UserContext);
  const [email, setEmail] = useState('employee@yopmail.com');
  const [password, setPassword] = useState('Admin123#');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [msgError, setMsgError] = useState('');

  store.clearAll();
  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true)
    const response = await AuthServices.login(email, password);
    if(response.status === 200){
      const responseUser = await AuthServices.getMe(response.data.access)
      const user = {...response.data, ...responseUser.data}

      store.set('user', user)
      if(user.is_superuser && user.is_staff && !user.manager){
        Router.push('/admin/users');
      }
      if(user.is_manager){
        Router.push('/manager/menus');
      }
      if(!user.is_manager && !user.is_superuser && !user.is_staff){
        Router.push('/employee/orders');
      }

    }else{
      setLoading(false)
      setMsgError("Invalid crendentials, try again.")
      setError(true)
    }
  }
  return (
    <>
      {loading ? <LoaderComponent/> : <Container>
      <Row>
        <Col>
          <br/>
          {error ? <Alert variant='danger'>
            {msgError}
          </Alert>: ''}
          <h3>Welcome system delivery manager</h3>
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control type="email" placeholder="Enter email" value='employee@yopmail.com'
                onChange={e => setEmail(e.target.value)} />
            </Form.Group>
            <Form.Group controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="Password" value='Admin123#'
                onChange={e => setPassword(e.target.value)} />
            </Form.Group>
            <br/>
            <Button variant="primary" type="submit" disabled={email.length <= 0 || password.length <= 0}>Login</Button>
          </Form>
        </Col >
      </Row >
    </Container >}
    </>


  )
}


