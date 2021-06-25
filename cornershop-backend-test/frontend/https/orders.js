import axios from 'axios';

export default new (class OrderServices {

  order_list(token) {
    axios.defaults.headers.common[
      'Authorization'
    ] = `Bearer ${token}`;
		return new Promise((resolve, reject) => {
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/orders/`,
				method: 'GET'
			})
				.then(resp => {
					resolve(resp);
				})
				.catch(err => {
					resolve(err);
				});
		});
	}

  order_delete(token, orderId) {
    axios.defaults.headers.common[
      'Authorization'
    ] = `Bearer ${token}`;
		return new Promise((resolve, reject) => {
			return axios({
				url: `${process.env.NEXT_PUBLIC_API_URL}api/v1/orders/${orderId}/`,
				method: 'DELETE'
			})
				.then(resp => {
					resolve(resp);
				})
				.catch(err => {
					reject(err.response.data);
				});
		});
	}
})();
