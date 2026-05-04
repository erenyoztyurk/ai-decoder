export interface ApiKeys {
  openai?: string;
  googleSearchConsole?: string;
  vercelToken?: string;
  cloudflareToken?: string;
  midjourneyApi?: string;
}

export interface ServiceStatus {
  service: keyof ApiKeys;
  isConfigured: boolean;
  lastChecked: Date;
}

export class ApiVault {
  private static instance: ApiVault;
  private keys: ApiKeys;

  private constructor() {
    this.keys = {
      openai: import.meta.env.OPENAI_API_KEY,
      googleSearchConsole: import.meta.env.GOOGLE_APPLICATION_CREDENTIALS,
      vercelToken: import.meta.env.VERCEL_ARTIFACTS_TOKEN,
      cloudflareToken: import.meta.env.CLOUDFLARE_API_TOKEN,
      midjourneyApi: import.meta.env.MIDJOURNEY_API_KEY,
    };
  }

  public static getInstance(): ApiVault {
    if (!ApiVault.instance) {
      ApiVault.instance = new ApiVault();
    }
    return ApiVault.instance;
  }

  public getKey(service: keyof ApiKeys): string {
    const key = this.keys[service];
    if (!key) {
      throw new Error(`API Kasası Hatası: ${service} anahtarı yapılandırılmamış.`);
    }
    return key;
  }

  public checkServiceStatus(): ServiceStatus[] {
    return (Object.keys(this.keys) as Array<keyof ApiKeys>).map((service) => ({
      service,
      isConfigured: !!this.keys[service],
      lastChecked: new Date(),
    }));
  }

  public async validateVercelConnection(): Promise<boolean> {
    try {
      const token = this.getKey("vercelToken");
      const response = await fetch("https://api.vercel.com/v9/projects", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.ok;
    } catch (error) {
      return false;
    }
  }

  public async validateOpenAIConnection(): Promise<boolean> {
    try {
      const token = this.getKey("openai");
      const response = await fetch("https://api.openai.com/v1/models", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.ok;
    } catch (error) {
      return false;
    }
  }

  public getMaskedKey(service: keyof ApiKeys): string {
    const key = this.keys[service];
    if (!key) return "YAPILANDIRILMADI";
    return `${key.substring(0, 4)}****************${key.substring(key.length - 4)}`;
  }
}

export const apiVault = ApiVault.getInstance(); 
