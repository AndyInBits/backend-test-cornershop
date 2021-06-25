import React, {useEffect, useState} from 'react'
import NavComponent from '../../components/NavComponent';
import {Container, Table, Button} from 'react-bootstrap';
import store from 'store-js';
import OrderServices from '../../https/orders';
import moment from 'moment';

const orders = () => {
  const user = store.get('user');
  const [loading, setLoading] = useState(false);
  const [orderList, setOrderList] = useState([]);
  const [reload, setReload] = useState(false);
  useEffect(() => {
    setLoading(true);
    if(!user || !user.is_manager){
      store.clearAll();
      Router.push('/');
    }
    OrderServices.order_list(user.access)
    .then(res => {
      setOrderList(res.data)
      setLoading(false)
    })
    .catch(() => {
      setLoading(false)
    })
  }, [reload]);

  async function DeleteOrder(menuId) {
    setLoading(true)
    OrderServices.order_delete(user.access, menuId)
    .then(() =>{
      setLoading(false)
      setReload(!reload)
    })
    .catch(() =>{
      setError(true)
    })
  };

  return (
    <>
      <NavComponent user={user}/>
      <Container>
      <h3>List Orders</h3>
      <Table striped bordered hover>
      <thead>
        <tr>
          <th>#</th>
          <th>Username</th>
          <th>User email</th>
          <th>Menu</th>
          <th>Comments</th>
          <th>Option</th>
          <th>Fecha</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
      {
        orderList.map(order =>{
            return (
              <tr key={order.pk}>
                <td>{order.pk}</td>
                <td>{order.user.username}</td>
                <td>{order.user.email}</td>
                <td>{order.menu.name}</td>
                <td>{order.comment}</td>
                <td>{order.option}</td>
                <td>{moment(order.created).format('YYYY-MM-DD')}</td>
                <td>
                <Button variant="danger" onClick={()=> {DeleteOrder(order.pk)}}>DEL</Button>
                </td>
              </tr>
            )
          })
        }
      </tbody>
    </Table>
      </Container>
    </>
  )
}

export default orders
