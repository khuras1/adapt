import { createClient } from '@supabase/supabase-js';

const supabaseUrl = "https://pemridpgtqunrjegyuac.supabase.co";
const supabaseKey = "sb_secret_SWqh9N0MOd7agOxnokvDkg_ID-UYxIR"; // For production, use env vars

export const supabase = createClient(supabaseUrl, supabaseKey);
