// back4app.js
import Parse from 'parse';

const PARSE_APPLICATION_ID = '89ltRwxuV57hVoVr6MaI8PxP6a3XYIBFlKvscMp5';
const PARSE_JAVASCRIPT_KEY = 'IY2O7w14ADqNYwwtHu1R14A6kUKSJwnzOn4SDNiG';
const PARSE_SERVER_URL = 'https://parseapi.back4app.com/';

Parse.initialize(PARSE_APPLICATION_ID, PARSE_JAVASCRIPT_KEY);
Parse.serverURL = PARSE_SERVER_URL;

export default Parse;