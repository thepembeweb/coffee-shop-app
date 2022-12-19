export const environment = {
  production: false,
  apiServerUrl: "http://127.0.0.1:5000", // the running FLASK api server url
  auth0: {
    url: "pembeweb.au", // the auth0 domain prefix
    audience: "CoffeeShop", // the audience set for the auth0 app
    clientId: "R5keb0Tyzm5kUZys5oDH7qTQzEiO4MkV", // the client id generated for the auth0 app
    callbackURL: "http://localhost:8100", // the base url of the running ionic application.
  },
};
