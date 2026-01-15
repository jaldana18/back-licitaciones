import { OpenAPIV3 } from 'openapi-types';

const swaggerSpec: OpenAPIV3.Document = {
  openapi: '3.0.0',
  info: {
    title: 'Sistema Licitaciones Salud API',
    version: '1.0.0',
    description: 'Documentación de la API para gestión de empresas, usuarios y licitaciones.'
  },
  servers: [
    { url: '/api', description: 'API local' }
  ],
  components: {
    securitySchemes: {
      bearerAuth: {
        type: 'http',
        scheme: 'bearer',
        bearerFormat: 'JWT',
      },
    },
  },
  security: [{ bearerAuth: [] }],
  paths: {
    '/auth/login': {
      post: {
        tags: ['Auth'],
        summary: 'Login de usuario',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                properties: {
                  email: { type: 'string' },
                  password: { type: 'string' }
                },
                required: ['email', 'password']
              }
            }
          }
        },
        responses: {
          '200': {
            description: 'Tokens generados',
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  properties: {
                    accessToken: { type: 'string' },
                    refreshToken: { type: 'string' }
                  }
                }
              }
            }
          },
          '401': { description: 'Credenciales inválidas' }
        }
      }
    },
    '/auth/refresh': {
      post: {
        tags: ['Auth'],
        summary: 'Renovar access token',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                type: 'object',
                properties: {
                  refreshToken: { type: 'string' }
                },
                required: ['refreshToken']
              }
            }
          }
        },
        responses: {
          '200': {
            description: 'Nuevo access token',
            content: {
              'application/json': {
                schema: {
                  type: 'object',
                  properties: {
                    accessToken: { type: 'string' }
                  }
                }
              }
            }
          },
          '401': { description: 'Refresh token inválido' }
        }
      }
    },
    '/companies': {
      get: {
        tags: ['Company'],
        summary: 'Listar empresas paginadas',
        parameters: [
          { name: 'page', in: 'query', schema: { type: 'integer' } },
          { name: 'limit', in: 'query', schema: { type: 'integer' } }
        ],
        responses: {
          '200': { description: 'Lista de empresas' }
        }
      },
      post: {
        tags: ['Company'],
        summary: 'Crear empresa',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                $ref: '#/components/schemas/Company'
              }
            }
          }
        },
        responses: {
          '201': { description: 'Empresa creada' }
        }
      }
    },
    '/companies/{id}': {
      get: {
        tags: ['Company'],
        summary: 'Obtener empresa por ID',
        parameters: [
          { name: 'id', in: 'path', required: true, schema: { type: 'string' } }
        ],
        responses: {
          '200': { description: 'Empresa encontrada' },
          '404': { description: 'No encontrada' }
        }
      },
      patch: {
        tags: ['Company'],
        summary: 'Actualizar empresa',
        parameters: [
          { name: 'id', in: 'path', required: true, schema: { type: 'string' } }
        ],
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                $ref: '#/components/schemas/Company'
              }
            }
          }
        },
        responses: {
          '200': { description: 'Empresa actualizada' },
          '404': { description: 'No encontrada' }
        }
      },
      delete: {
        tags: ['Company'],
        summary: 'Eliminar empresa',
        parameters: [
          { name: 'id', in: 'path', required: true, schema: { type: 'string' } }
        ],
        responses: {
          '200': { description: 'Empresa eliminada' },
          '404': { description: 'No encontrada' }
        }
      }
    },
    '/users': {
      get: {
        tags: ['User'],
        summary: 'Listar usuarios paginados',
        parameters: [
          { name: 'page', in: 'query', schema: { type: 'integer' } },
          { name: 'limit', in: 'query', schema: { type: 'integer' } }
        ],
        responses: {
          '200': { description: 'Lista de usuarios' }
        }
      },
      post: {
        tags: ['User'],
        summary: 'Crear usuario',
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                $ref: '#/components/schemas/User'
              }
            }
          }
        },
        responses: {
          '201': { description: 'Usuario creado' }
        }
      }
    },
    '/users/{id}': {
      get: {
        tags: ['User'],
        summary: 'Obtener usuario por ID',
        parameters: [
          { name: 'id', in: 'path', required: true, schema: { type: 'string' } }
        ],
        responses: {
          '200': { description: 'Usuario encontrado' },
          '404': { description: 'No encontrado' }
        }
      },
      patch: {
        tags: ['User'],
        summary: 'Actualizar usuario',
        parameters: [
          { name: 'id', in: 'path', required: true, schema: { type: 'string' } }
        ],
        requestBody: {
          required: true,
          content: {
            'application/json': {
              schema: {
                $ref: '#/components/schemas/User'
              }
            }
          }
        },
        responses: {
          '200': { description: 'Usuario actualizado' },
          '404': { description: 'No encontrado' }
        }
      },
      delete: {
        tags: ['User'],
        summary: 'Eliminar usuario',
        parameters: [
          { name: 'id', in: 'path', required: true, schema: { type: 'string' } }
        ],
        responses: {
          '200': { description: 'Usuario eliminado' },
          '404': { description: 'No encontrado' }
        }
      }
    }
  },
  components: {
    schemas: {
      Company: {
        type: 'object',
        properties: {
          name: { type: 'string' },
          nit: { type: 'string' },
          sector: { type: 'string' },
          email: { type: 'string' },
          phone: { type: 'string' },
          address: { type: 'string' },
          isActive: { type: 'boolean' }
        }
      },
      User: {
        type: 'object',
        properties: {
          companyId: { type: 'string' },
          name: { type: 'string' },
          email: { type: 'string' },
          password: { type: 'string' },
          role: { type: 'string', enum: ['admin', 'user', 'viewer'] },
          isActive: { type: 'boolean' }
        }
      }
    }
  }
};

export default swaggerSpec;
