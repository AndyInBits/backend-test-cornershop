import React, {useEffect, useState} from 'react'
import { useRouter } from 'next/router'
import {Jumbotron, Button, Container,Form, Alert} from 'react-bootstrap';
import MenuTodayServices from '../../https/menu';
import LoaderComponent from '../../components/LoaderComponent';
import NavComponent from '../../components/NavComponent';


const menu = () => {
  const router = useRouter();
  const [error, setError] = useState(false);
  const [errorData, setErrorData] = useState(true);
  const [msgError, setMsgError] = useState('');
  const [loading, setLoading] = useState(false);
  const [menu, setMenu] = useState({name: '', options: []});
  const { uuid } = router.query

  const [success, setSuccess] = useState(false);
  const [msgSuccess, setMsgSuccess] = useState('');
  const [comments, setComments] = useState('');
  const [email, setEmail] = useState('');
  const [options, setOptions] = useState('0');
  const [password, setPassword] = useState('');

  const getOptions = () => {
    return menu.options.map(opt => {
      return <option key={opt.pk} value={opt.opcion}>{opt.option}</option>
    })
  }

  const createOrderHandleSubmit = async (event) => {
    event.preventDefault();

    const body = {
      menu: menu.pk,
      comment: comments,
      email,
      password,
      option: options
    }
    MenuTodayServices.create_order(body)
    .then(res =>{
      setSuccess(true)
      setMsgSuccess(res.data.detail)
      setLoading(false)
    })
    .catch( err =>{
      setError(true)
      setMsgError(JSON.stringify(err))
      setLoading(false)
    })
  }
  useEffect( () => {
    if(uuid){
      setLoading(true)
      MenuTodayServices.menu_today(uuid)
      .then(res => {
        setMenu(res.data)
        setErrorData(false)
        setLoading(false)

      })
      .catch(() => {
        setErrorData(true)
        setLoading(false)
      })
    }
  }, [router]);

  return (
    <>
    {loading ? <LoaderComponent/> :

    <>
    <NavComponent/>
    <Container>

    <br/>
    {success ? <Alert variant='success'>
            {msgSuccess}
          </Alert>: ''}
    {error ? <Alert variant='danger'>
            {msgError}
          </Alert>: ''}
    <br/>
      { !errorData ?
      (<Jumbotron>
          <h1>Hello, This menu today !</h1>
          <h3>
            {menu?.name}
          </h3>
          <p>
          OPTIONS :
            <ul>
            {menu?.options.map(opt => {
              return (
                  <li key={opt.pk}>
                    {opt.option}
                  </li>)
            })}
            </ul>
          </p>
          <br/>
          <hr/>
          <p>
          <h1>Make an order</h1>
          <Form onSubmit={createOrderHandleSubmit}>
          <Form.Group controlId="formBasicmenuemail">
              <Form.Label>Email user</Form.Label>
              <Form.Control type="email" placeholder="Enter your email"
                onChange={e => setEmail(e.target.value)}
              />
            <br/>
            </Form.Group>
            <Form.Group controlId="formBasicPassword">
              <Form.Label>Password user</Form.Label>
              <Form.Control type="password" placeholder="Enter your Password"
                onChange={e => setPassword(e.target.value)} />
            </Form.Group>
            <br/>
            <Form.Group controlId="formBasicmenuName">
              <Form.Label>Additional comments</Form.Label>
              <Form.Control type="text" placeholder="Enter comments"
                onChange={e => setComments(e.target.value)}
              />
            </Form.Group>
            <br/>
            <Form.Group controlId="exampleForm.ControlSelect1">
              <Form.Label>Select Option</Form.Label>
              <Form.Control as="select" onChange={e => setOptions(e.target.value)}>
                 <option value="0">Select Option</option>
                  {getOptions()}
              </Form.Control>
            </Form.Group>

            <br/>
            <br/>
            <Button variant="primary" type="submit"disabled={!comments || !email || options==="0" || !password }>Order</Button>
          </Form>

          </p>
        </Jumbotron> ) :

        (<Jumbotron>
          <h1>This menu is no longer available !</h1>
        </Jumbotron>)
      }
    </Container>
    </>
    }
    </>
  )
}

export default menu;
