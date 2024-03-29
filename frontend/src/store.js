import { combineReducers, configureStore } from '@reduxjs/toolkit';
import {thunk} from 'redux-thunk'; // Correct the import statement
import {userLoginReducer} from './reducers/userReducers'; // Correct the import statement
import {userSendChangePasswordReducer} from './reducers/userReducers'; // Correct the import statement
import {userRegisterReducer} from './reducers/userReducers'; // Correct the import statement
import {userConfirmChangePasswordReducer} from './reducers/userReducers'; // Correct the import statement

const reducer = combineReducers({
    userLogin: userLoginReducer,
    userRegister: userRegisterReducer,
    userSendChangePassword: userSendChangePasswordReducer,
    userConfirmChangePassword: userConfirmChangePasswordReducer,
});

const initialState = {
    userLogin: {
        userInfo: localStorage.getItem('userInfo')
            ? JSON.parse(localStorage.getItem('userInfo'))
            : null,
    },

};

const middleware = [thunk];

const store = configureStore({
    reducer,
    preloadedState: initialState, // Correct the property name to preloadedState
    middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(middleware),
});

export default store;
