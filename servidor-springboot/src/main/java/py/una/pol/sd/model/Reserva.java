package py.una.pol.sd.model;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Entity
public class Reserva {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private Long usuarioId; // relación simple con Usuario
    private Long viajeId; // relación simple con Viaje
    private String estado; // "pendiente", "confirmada", "cancelada"
    private String fechaReserva;

    public Reserva() {}

    public Reserva(Long usuarioId, Long viajeId, String estado, String fechaReserva) {
        this.usuarioId = usuarioId;
        this.viajeId = viajeId;
        this.estado = estado;
        this.fechaReserva = fechaReserva;
    }

    // getters y setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Long getUsuarioId() { return usuarioId; }
    public void setUsuarioId(Long usuarioId) { this.usuarioId = usuarioId; }

    public Long getViajeId() { return viajeId; }
    public void setViajeId(Long viajeId) { this.viajeId = viajeId; }

    public String getEstado() { return estado; }
    public void setEstado(String estado) { this.estado = estado; }

    public String getFechaReserva() { return fechaReserva; }
    public void setFechaReserva(String fechaReserva) { this.fechaReserva = fechaReserva; }
}
