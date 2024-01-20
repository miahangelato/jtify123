import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import { useDispatch } from 'react-redux';
import { login } from '../../actions/userActions';
import FormContainer from '../FormContainer';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import { useSelector } from 'react-redux';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const userLogin = useSelector((state) => state.userLogin);
    const { userInfo } = userLogin;

    let navigate = useNavigate();
    const dispatch = useDispatch();
    useEffect(() => {
        if (userInfo) {
            navigate('/home');
        }
    }, [navigate, userInfo]);


    const submitHandler = (e) => {
        e.preventDefault();

        // Dispatch the login action with the provided email and password
        dispatch(login(email, password));
    };

    return (
        <FormContainer>
            <h1>Sign In</h1>
            <Form onSubmit={submitHandler}>
                <Form.Group controlId='email'>
                    <Form.Label>Email Address</Form.Label>
                    <Form.Control
                        type='email'
                        placeholder='Enter email'
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    ></Form.Control>
                </Form.Group>

                <Form.Group controlId='password'>
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        type='password'
                        placeholder='Enter password'
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    ></Form.Control>
                </Form.Group>

                <Button type='submit' variant='primary'>
                    Sign In
                </Button>
            </Form>
        </FormContainer>
    );
}

export default Login;
