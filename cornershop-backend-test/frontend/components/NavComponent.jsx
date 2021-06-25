import React from 'react'
import {Nav,Navbar, Container} from 'react-bootstrap';
import store from 'store-js'
import Router from 'next/router';

const NavComponent = ({user}) => {

  const logout = () => {
    store.clearAll();
    Router.push('/');
  };

  return (
    <Navbar bg="light" expand="lg">
        <Container>
        <Navbar.Brand href="#">System Delivery  </Navbar.Brand>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
              <Navbar.Collapse id="responsive-navbar-nav">
              <Nav className="me-auto">
                {user?.is_staff ?
                  <Nav.Link href="/admin/users">Users</Nav.Link>
                : ''
                }
                {user?.is_manager ?
                 <>
                  <Nav.Link href="/manager/menus">Menus</Nav.Link>
                  <Nav.Link href="/manager/orders">Orders</Nav.Link>
                  </>
                : ''
                }
                </Nav>

                <Nav>
                {user ?
                  <Nav.Link eventKey={2} onClick={logout}>
                  @{user?.username ||'Anonimus'}  -  Logout
                  </Nav.Link> :
                  <Nav.Link eventKey={2} href="/">
                  Login
                  </Nav.Link>}
                </Nav>
              </Navbar.Collapse>
        </Container>
    </Navbar>
  )
}

export default NavComponent
