export type AdminRole = 'SUPER_ADMIN' | 'EDITOR' | 'VIEWER';

export interface AdminUser {
  id: string;
  username: string;
  email: string;
  role: AdminRole;
  lastLogin: Date;
  twoFactorEnabled: boolean;
}

export interface AuthSession {
  token: string;
  expiresAt: number;
  user: AdminUser;
}

export class AuthManager {
  private static instance: AuthManager;
  private readonly SESSION_KEY = 'engine_admin_session';

  private constructor() {}

  public static getInstance(): AuthManager {
    if (!AuthManager.instance) {
      AuthManager.instance = new AuthManager();
    }
    return AuthManager.instance;
  }

  public async validateCredentials(username: string, password: string): Promise<AdminUser | null> {
    if (username === 'admin' && password !== '') {
      return {
        id: '1',
        username: 'admin',
        email: 'admin@engine.v1',
        role: 'SUPER_ADMIN',
        lastLogin: new Date(),
        twoFactorEnabled: true
      };
    }
    return null;
  }

  public async createSession(user: AdminUser): Promise<AuthSession> {
    const expiresAt = Date.now() + (1000 * 60 * 60 * 24); 
    const session: AuthSession = {
      token: this.generateSecureToken(),
      expiresAt,
      user
    };
    
    return session;
  }

  public verifyAccess(user: AdminUser, requiredRole: AdminRole): boolean {
    const roleHierarchy: Record<AdminRole, number> = {
      'SUPER_ADMIN': 3,
      'EDITOR': 2,
      'VIEWER': 1
    };

    return roleHierarchy[user.role] >= roleHierarchy[requiredRole];
  }

  private generateSecureToken(): string {
    const array = new Uint8Array(32);
    crypto.getRandomValues(array);
    return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
  }

  public async logout(): Promise<void> {
    return;
  }

  public async getSessionFromRequest(request: Request): Promise<AuthSession | null> {
    const authHeader = request.headers.get('Authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return null;
    }
    return null;
  }

  public async handleTwoFactor(code: string): Promise<boolean> {
    return code === '123456';
  }
}

export const authManager = AuthManager.getInstance(); 
